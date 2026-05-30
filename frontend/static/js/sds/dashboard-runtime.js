(function () {
  const api = () => window.sds && window.sds.apiClient;

  const root = document.querySelector('[data-dashboard-role]');
  if (!root || !api()) {
    return;
  }

  const role = (root.dataset.dashboardRole || '').toLowerCase();
  const currentUserId = document.body.dataset.userId || '';

  const state = {
    roles: [],
    users: [],
    aulas: [],
    grupos: [],
    docentes: [],
    cursos: [],
    bloques: [],
    reservas: [],
    parametros: [],
  };

  let refreshTimer = null;
  let adminBound = false;
  let leaderBound = false;
  let auxiliarBound = false;
  let facultyBound = false;
  let admissionsBound = false;

  const esc = (value) =>
    String(value ?? '')
      .replaceAll('&', '&amp;')
      .replaceAll('<', '&lt;')
      .replaceAll('>', '&gt;')
      .replaceAll('"', '&quot;')
      .replaceAll("'", '&#39;');

  const showStatus = (id, message, tone = 'info') => {
    const el = document.getElementById(id);
    if (!el) return;
    el.textContent = message;
    el.dataset.tone = tone;
  };

  const toast = (type, message) => {
    if (window.sds?.toast?.show) {
      window.sds.toast.show({ type, message });
    }
  };

  const toIso = (value) => {
    if (!value) return '';
    return new Date(value).toISOString();
  };

  const fmtDate = (value) => {
    if (!value) return '';
    try {
      return new Date(value).toLocaleString('es-CO', {
        dateStyle: 'short',
        timeStyle: 'short',
      });
    } catch (_) {
      return String(value);
    }
  };

  const renderTable = (tbodyId, rowsHtml, emptyLabel = 'Sin registros') => {
    const tbody = document.getElementById(tbodyId);
    if (!tbody) return;
    tbody.innerHTML = rowsHtml || `<tr><td colspan="6">${esc(emptyLabel)}</td></tr>`;
  };

  const renderOptions = (selectId, options, { placeholder = 'Selecciona una opcion', valueKey = 'id', labelFn }) => {
    const select = document.getElementById(selectId);
    if (!select) return;
    const rows = [
      `<option value="">${esc(placeholder)}</option>`,
      ...options.map((item) => {
        const label = labelFn ? labelFn(item) : item[valueKey];
        return `<option value="${esc(item[valueKey])}">${esc(label)}</option>`;
      }),
    ];
    select.innerHTML = rows.join('');
  };

  const fetchJson = async (url) => api().get(url);

  const postJson = async (url, body) => api().post(url, body);

  const normalizeCheckbox = (form, name) => {
    const field = form.querySelector(`[name="${name}"]`);
    return field ? field.checked : false;
  };

  const normalizeText = (value) =>
    String(value ?? '')
      .toLowerCase()
      .normalize('NFD')
      .replace(/[\u0300-\u036f]/g, '');

  const formDataObject = (form) => {
    const data = {};
    const fd = new FormData(form);
    for (const [key, value] of fd.entries()) {
      if (typeof value === 'string') {
        data[key] = value.trim();
      } else {
        data[key] = value;
      }
    }
    return data;
  };

  const loadCatalog = async () => {
    const [roles, users, aulas, grupos, docentes, cursos, bloques, reservas, parametros] = await Promise.all([
      fetchJson('/api/usuarios/catalogo-roles/').catch(() => []),
      fetchJson('/api/usuarios/lista/').catch(() => []),
      fetchJson('/api/academico/aulas/').catch(() => []),
      fetchJson('/api/academico/aulas/grupos/').catch(() => []),
      fetchJson('/api/academico/aulas/docentes/').catch(() => []),
      fetchJson('/api/academico/aulas/cursos/').catch(() => []),
      fetchJson('/api/academico/aulas/bloques/').catch(() => []),
      fetchJson('/api/reservas/').catch(() => []),
      fetchJson('/api/parametros/').catch(() => []),
    ]);

    state.roles = roles;
    state.users = users;
    state.aulas = aulas;
    state.grupos = grupos;
    state.docentes = docentes;
    state.cursos = cursos;
    state.bloques = bloques;
    state.reservas = reservas;
    state.parametros = parametros;
  };

  const renderCurrentPanel = () => {
    if (role === 'administrador') {
      renderAdmin();
    } else if (role === 'lider_sd' || role === 'lider_doc') {
      renderLeader();
    } else if (role === 'auxiliar_sd' || role === 'auxiliar_doc') {
      renderAuxiliar();
    } else if (role === 'facultad') {
      renderFaculty();
    } else if (role === 'admisiones') {
      renderAdmissions();
    }
  };

  const refreshCurrentPanel = async () => {
    await loadCatalog();
    renderCurrentPanel();
  };

  const scheduleRefresh = () => {
    window.clearTimeout(refreshTimer);
    refreshTimer = window.setTimeout(() => {
      refreshCurrentPanel().catch((error) => {
        toast('error', error.details || error.message || 'No se pudo refrescar el panel.');
      });
    }, 180);
  };

  const refreshLeaderCoverage = async (semestre) => {
    const data = await fetchJson(`/api/asignacion/cobertura/?semestre=${encodeURIComponent(semestre)}`);
    const total = Number(data?.total_grupos || 0);
    const asignados = Number(data?.grupos_con_aula || 0);
    const percentage = total > 0 ? Math.round((asignados / total) * 100) : 0;
    const el = document.getElementById('leader-cobertura-text');
    if (el) {
      el.textContent = `${asignados} de ${total} grupos con aula (${percentage}%)`;
    }
  };

  const renderAdmin = () => {
    renderOptions(
      'admin-user-role',
      state.roles,
      {
        placeholder: 'Selecciona un rol',
        valueKey: 'code',
        labelFn: (item) => `${item.name} (${item.code})`,
      }
    );

    renderTable(
      'admin-roles-body',
      state.roles
        .map(
          (roleItem) =>
            `<tr><td>${esc(roleItem.code)}</td><td>${esc(roleItem.name)}</td><td>${esc(roleItem.description || '')}</td></tr>`
        )
        .join('')
    );

    renderTable(
      'admin-users-body',
      state.users
        .map(
          (user) =>
            `<tr><td>${esc(user.username)}</td><td>${esc(user.role_name || user.role_code || '')}</td><td>${esc(user.email)}</td></tr>`
        )
        .join('')
    );

    renderTable(
      'admin-aulas-body',
      state.aulas
        .map(
          (aula) =>
            `<tr><td>${esc(aula.nombre)}</td><td>${esc(aula.capacidad)}</td><td>${esc(aula.tipo)}</td><td><span class="badge ${aula.disponible ? 'badge-success' : 'badge-warning'}">${aula.disponible ? 'Disponible' : 'Ocupada'}</span></td></tr>`
        )
        .join(''),
      'No hay aulas registradas'
    );

    renderTable(
      'admin-param-body',
      state.parametros
        .map(
          (parametro) =>
            `<tr><td>${esc(parametro.clave)}</td><td>${esc(parametro.grupo)}</td><td><code>${esc(JSON.stringify(parametro.valor))}</code></td><td><span class="badge ${parametro.activo ? 'badge-success' : 'badge-warning'}">${parametro.activo ? 'Activo' : 'Inactivo'}</span></td></tr>`
        )
        .join(''),
      'No hay parametros configurados'
    );
  };

  const bindAdmin = () => {
    if (adminBound) return;
    adminBound = true;
    const roleForm = document.getElementById('admin-role-form');
    const userForm = document.getElementById('admin-user-form');
    const aulaForm = document.getElementById('admin-aula-form');
    const paramForm = document.getElementById('admin-param-form');

    roleForm?.addEventListener('submit', async (evt) => {
      evt.preventDefault();
      const data = formDataObject(roleForm);
      try {
        await postJson('/api/usuarios/catalogo-roles/', data);
        showStatus('admin-role-status', 'Rol guardado correctamente.', 'success');
        toast('success', 'Rol guardado correctamente.');
        await loadCatalog();
        await refreshCurrentPanel();
      } catch (error) {
        showStatus('admin-role-status', error.details || error.message, 'error');
        toast('error', error.details || 'No se pudo guardar el rol.');
      }
    });

    userForm?.addEventListener('submit', async (evt) => {
      evt.preventDefault();
      const data = formDataObject(userForm);
      try {
        await postJson('/api/usuarios/crear/', data);
        showStatus('admin-user-status', 'Usuario creado correctamente.', 'success');
        toast('success', 'Usuario creado correctamente.');
        await loadCatalog();
        await refreshCurrentPanel();
      } catch (error) {
        showStatus('admin-user-status', error.details || error.message, 'error');
        toast('error', error.details || 'No se pudo crear el usuario.');
      }
    });

    aulaForm?.addEventListener('submit', async (evt) => {
      evt.preventDefault();
      const data = formDataObject(aulaForm);
      data.capacidad = Number(data.capacidad);
      data.disponible = normalizeCheckbox(aulaForm, 'disponible');
      try {
        await postJson('/api/academico/aulas/', data);
        showStatus('admin-aula-status', 'Aula creada correctamente.', 'success');
        toast('success', 'Aula creada correctamente.');
        await loadCatalog();
        await refreshCurrentPanel();
      } catch (error) {
        showStatus('admin-aula-status', error.details || error.message, 'error');
        toast('error', error.details || 'No se pudo crear el aula.');
      }
    });

    paramForm?.addEventListener('submit', async (evt) => {
      evt.preventDefault();
      const data = formDataObject(paramForm);
      try {
        data.valor = JSON.parse(data.valor);
      } catch (_) {
        showStatus('admin-param-status', 'El valor debe ser JSON valido.', 'error');
        return;
      }
      data.activo = normalizeCheckbox(paramForm, 'activo');
      try {
        await postJson('/api/parametros/', data);
        showStatus('admin-param-status', 'Parametro guardado correctamente.', 'success');
        toast('success', 'Parametro guardado correctamente.');
        await loadCatalog();
        await refreshCurrentPanel();
      } catch (error) {
        showStatus('admin-param-status', error.details || error.message, 'error');
        toast('error', error.details || 'No se pudo guardar el parametro.');
      }
    });
  };

  const renderLeader = async () => {
    renderOptions('leader-grupo-select', state.grupos, {
      placeholder: 'Selecciona un grupo',
      valueKey: 'id',
      labelFn: (item) => `${item.codigo} - ${item.curso_nombre || 'Materia'} - ${item.num_estudiantes} estudiantes`,
    });
    renderOptions('leader-aula-select', state.aulas, {
      placeholder: 'Selecciona un aula',
      valueKey: 'id',
      labelFn: (item) => `${item.nombre} (${item.capacidad})`,
    });
    renderOptions('leader-bloque-select', state.bloques, {
      placeholder: 'Selecciona un bloque',
      valueKey: 'id',
      labelFn: (item) => `${item.dia} ${item.hora_inicio} - ${item.hora_fin}`,
    });

    renderTable(
      'leader-grupos-body',
      state.grupos
        .map(
          (grupo) =>
            `<tr><td>${esc(grupo.codigo)}</td><td>${esc(grupo.curso_nombre || grupo.curso_codigo || '')}</td><td>${esc(grupo.num_estudiantes)}</td><td>${esc(grupo.semestre)}</td></tr>`
        )
        .join(''),
      'No hay grupos cargados'
    );

    renderTable(
      'leader-aulas-body',
      state.aulas
        .map(
          (aula) =>
            `<tr><td>${esc(aula.nombre)}</td><td>${esc(aula.capacidad)}</td><td><span class="badge ${aula.disponible ? 'badge-success' : 'badge-warning'}">${aula.disponible ? 'Si' : 'No'}</span></td></tr>`
        )
        .join(''),
      'No hay aulas disponibles'
    );
  };

  const bindLeader = () => {
    if (leaderBound) return;
    leaderBound = true;
    const execForm = document.getElementById('leader-exec-form');
    const simForm = document.getElementById('leader-sim-form');
    const semesterAssignButton = document.getElementById('leader-semester-assign');

    execForm?.addEventListener('submit', async (evt) => {
      evt.preventDefault();
      const data = formDataObject(execForm);
      try {
        const result = await postJson('/api/asignacion/ejecutar/', data);
        showStatus('leader-exec-status', `Asignacion confirmada para ${result.semestre}.`, 'success');
        toast('success', 'Asignacion ejecutada correctamente.');
        await refreshCurrentPanel();
        await refreshLeaderCoverage(data.semestre);
      } catch (error) {
        showStatus('leader-exec-status', error.details || error.message, 'error');
        toast('error', error.details || 'No se pudo ejecutar la asignacion.');
      }
    });

    simForm?.addEventListener('submit', async (evt) => {
      evt.preventDefault();
      const data = formDataObject(simForm);
      try {
        const result = await postJson('/api/asignacion/simular-semestre/', {
          semestre: data.semestre,
        });
        const asignables = result.asignaciones?.filter((item) => item.estado !== 'PENDIENTE').length || 0;
        const pendientes = result.asignaciones?.filter((item) => item.estado === 'PENDIENTE').length || 0;
        showStatus(
          'leader-sim-status',
          `${result.mensaje || 'Simulacion completada.'} Asignables: ${asignables}. Pendientes: ${pendientes}.`,
          pendientes > 0 ? 'warning' : 'success'
        );
        toast('success', 'Simulacion ejecutada.');
        await refreshCurrentPanel();
        await refreshLeaderCoverage(data.semestre);
      } catch (error) {
        showStatus('leader-sim-status', error.details || error.message, 'error');
        toast('error', error.details || 'No se pudo simular la asignacion.');
      }
    });

    semesterAssignButton?.addEventListener('click', async () => {
      const data = formDataObject(simForm);
      try {
        const result = await postJson('/api/asignacion/ejecutar-semestre/', {
          semestre: data.semestre,
        });
        const pendientes = Number(result.grupos_pendientes || 0);
        showStatus(
          'leader-sim-status',
          `${result.total_asignaciones || 0} grupos asignados. Pendientes: ${pendientes}.`,
          pendientes > 0 ? 'warning' : 'success'
        );
        toast(pendientes > 0 ? 'warning' : 'success', 'Asignacion de semestre finalizada.');
        await refreshCurrentPanel();
        await refreshLeaderCoverage(data.semestre);
      } catch (error) {
        showStatus('leader-sim-status', error.details || error.message, 'error');
        toast('error', error.details || 'No se pudo asignar el semestre.');
      }
    });
  };

  const renderAuxiliar = () => {
    const aulaFilter = normalizeText(document.getElementById('aux-aula-filter')?.value || '');
    const aulasFiltradas = aulaFilter
      ? state.aulas.filter((aula) => {
          const haystack = normalizeText(
            [aula.nombre, aula.capacidad, aula.tipo, aula.disponible ? 'disponible' : 'ocupada']
              .filter(Boolean)
              .join(' ')
          );
          return haystack.includes(aulaFilter);
        })
      : state.aulas;

    renderOptions('aux-reserva-aula', state.aulas, {
      placeholder: 'Selecciona un aula',
      valueKey: 'id',
      labelFn: (item) => `${item.nombre} (${item.capacidad})`,
    });

    const solicitante = document.getElementById('aux-reserva-solicitante');
    if (solicitante && currentUserId) {
      solicitante.value = currentUserId;
      solicitante.readOnly = true;
    }

    renderTable(
      'aux-aulas-body',
      aulasFiltradas
        .map(
          (aula) =>
            `<tr><td>${esc(aula.nombre)}</td><td>${esc(aula.capacidad)}</td><td><span class="badge ${aula.disponible ? 'badge-success' : 'badge-warning'}">${aula.disponible ? 'Disponible' : 'Ocupada'}</span></td></tr>`
        )
        .join(''),
      aulaFilter ? 'No hay aulas que coincidan con el filtro' : 'No hay aulas registradas'
    );

    renderTable(
      'aux-reservas-body',
      state.reservas
        .map(
          (reserva) =>
            `<tr>
              <td>${esc(reserva.reserva_id)}</td>
              <td>${esc(reserva.aula_id)}</td>
              <td><span class="badge ${reserva.estado === 'confirmed' || reserva.estado === 'CONFIRMADA' ? 'badge-success' : 'badge-warning'}">${esc(reserva.estado)}</span></td>
              <td>
                <div class="hero-actions">
                  <button class="btn btn-ghost" type="button" data-reserva-confirm="${esc(reserva.reserva_id)}">Confirmar</button>
                  <button class="btn btn-ghost" type="button" data-reserva-cancel="${esc(reserva.reserva_id)}">Cancelar</button>
                </div>
              </td>
            </tr>`
        )
        .join(''),
      'No hay reservas registradas'
    );

    document.querySelectorAll('[data-reserva-confirm]').forEach((button) => {
      button.addEventListener('click', async () => {
        const reservaId = button.getAttribute('data-reserva-confirm');
        try {
          await postJson(`/api/reservas/${reservaId}/confirmar/`, {});
          toast('success', 'Reserva confirmada.');
          await loadCatalog();
          renderAuxiliar();
        } catch (error) {
          toast('error', error.details || 'No se pudo confirmar la reserva.');
        }
      });
    });

    document.querySelectorAll('[data-reserva-cancel]').forEach((button) => {
      button.addEventListener('click', async () => {
        const reservaId = button.getAttribute('data-reserva-cancel');
        try {
          await postJson(`/api/reservas/${reservaId}/cancelar/`, {});
          toast('success', 'Reserva cancelada.');
          await loadCatalog();
          renderAuxiliar();
        } catch (error) {
          toast('error', error.details || 'No se pudo cancelar la reserva.');
        }
      });
    });
  };

  const bindAuxiliar = () => {
    if (auxiliarBound) return;
    auxiliarBound = true;
    const form = document.getElementById('aux-reserva-form');
    const aulaFilter = document.getElementById('aux-aula-filter');
    const clearFilter = document.getElementById('aux-aula-filter-clear');

    aulaFilter?.addEventListener('input', () => {
      renderAuxiliar();
    });

    clearFilter?.addEventListener('click', () => {
      if (aulaFilter) {
        aulaFilter.value = '';
      }
      renderAuxiliar();
      aulaFilter?.focus();
    });

    form?.addEventListener('submit', async (evt) => {
      evt.preventDefault();
      const data = formDataObject(form);
      data.inicio = toIso(data.inicio);
      data.fin = toIso(data.fin);
      if (!data.solicitante_id) {
        data.solicitante_id = currentUserId;
      }
      try {
        await postJson('/api/reservas/', data);
        showStatus('aux-reserva-status', 'Reserva creada correctamente.', 'success');
        toast('success', 'Reserva creada correctamente.');
        await refreshCurrentPanel();
      } catch (error) {
        showStatus('aux-reserva-status', error.details || error.message, 'error');
        toast('error', error.details || 'No se pudo crear la reserva.');
      }
    });
  };

  const renderFaculty = () => {
    renderOptions('faculty-curso-select', state.cursos, {
      placeholder: 'Selecciona un curso',
      valueKey: 'id',
      labelFn: (item) => `${item.codigo} - ${item.nombre}`,
    });
    renderOptions('faculty-docente-select', state.docentes, {
      placeholder: 'Selecciona un docente',
      valueKey: 'id',
      labelFn: (item) => `${item.nombre} - ${item.email}`,
    });

    renderTable(
      'faculty-aulas-body',
      state.aulas
        .map(
          (aula) =>
            `<tr><td>${esc(aula.nombre)}</td><td>${esc(aula.capacidad)}</td><td><span class="badge ${aula.disponible ? 'badge-success' : 'badge-warning'}">${aula.disponible ? 'Disponible' : 'Ocupada'}</span></td></tr>`
        )
        .join(''),
      'No hay aulas registradas'
    );

    renderTable(
      'faculty-grupos-body',
      state.grupos
        .map(
          (grupo) =>
            `<tr><td>${esc(grupo.codigo)}</td><td>${esc(grupo.curso_nombre || grupo.curso_codigo || '')}</td><td>${esc(grupo.num_estudiantes)}</td><td>${esc(grupo.semestre)}</td></tr>`
        )
        .join(''),
      'No hay grupos registrados'
    );

    const docentesText = document.getElementById('faculty-docentes-text');
    if (docentesText) {
      docentesText.textContent = `${state.docentes.length} docentes disponibles para asignacion.`;
    }

    const cursosText = document.getElementById('faculty-cursos-text');
    if (cursosText) {
      cursosText.textContent = `${state.cursos.length} cursos activos listos para grupos.`;
    }
  };

  const bindFaculty = () => {
    if (facultyBound) return;
    facultyBound = true;
    const form = document.getElementById('faculty-grupo-form');
    form?.addEventListener('submit', async (evt) => {
      evt.preventDefault();
      const data = formDataObject(form);
      data.num_estudiantes = Number(data.num_estudiantes);
      try {
        await postJson('/api/academico/aulas/grupos/', data);
        showStatus('faculty-grupo-status', 'Grupo guardado correctamente.', 'success');
        toast('success', 'Grupo guardado correctamente.');
        await refreshCurrentPanel();
      } catch (error) {
        showStatus('faculty-grupo-status', error.details || error.message, 'error');
        toast('error', error.details || 'No se pudo guardar el grupo.');
      }
    });
  };

  const renderAdmissions = () => {
    renderTable(
      'admissions-grupos-body',
      state.grupos
        .map(
          (grupo) =>
            `<tr><td>${esc(grupo.codigo)}</td><td>${esc(grupo.curso_nombre || grupo.curso_codigo || '')}</td><td>${esc(grupo.num_estudiantes)}</td><td>${esc(grupo.semestre)}</td><td><span class="badge ${grupo.activo ? 'badge-success' : 'badge-warning'}">${grupo.activo ? 'Activo' : 'Inactivo'}</span></td></tr>`
        )
        .join(''),
      'No hay grupos cargados'
    );
  };

  const bindAdmissions = () => {
    if (admissionsBound) return;
    admissionsBound = true;
    const form = document.getElementById('admissions-bulk-form');
    form?.addEventListener('submit', async (evt) => {
      evt.preventDefault();
      const bulkRows = document.getElementById('admissions-bulk-rows');
      const rows = (bulkRows?.value || '')
        .split('\n')
        .map((line) => line.trim())
        .filter(Boolean);

      if (!rows.length) {
        showStatus('admissions-bulk-status', 'Agrega al menos una linea con datos del grupo.', 'error');
        return;
      }

      let successCount = 0;
      let errorCount = 0;

      for (const line of rows) {
        const [curso_id, docente_id, codigo, num_estudiantes, semestre] = line.split(',').map((item) => item.trim());
        try {
          await postJson('/api/academico/aulas/grupos/', {
            curso_id,
            docente_id,
            codigo,
            num_estudiantes: Number(num_estudiantes),
            semestre,
          });
          successCount += 1;
        } catch (error) {
          errorCount += 1;
        }
      }

      const total = rows.length;
      const percent = total > 0 ? Math.round((successCount / total) * 100) : 0;
      const fill = document.getElementById('admissions-progress-fill');
      const progress = document.getElementById('admissions-progress-text');
      if (fill) fill.style.width = `${percent}%`;
      if (progress) progress.textContent = `${percent}%`;

      showStatus(
        'admissions-bulk-status',
        `${successCount} grupos guardados y ${errorCount} registros con error.`,
        errorCount > 0 ? 'warning' : 'success'
      );
      toast(errorCount > 0 ? 'warning' : 'success', 'Procesamiento de lote finalizado.');
      await refreshCurrentPanel();
    });
  };

  const boot = async () => {
    try {
      await refreshCurrentPanel();
      if (role === 'administrador') {
        bindAdmin();
      } else if (role === 'lider_sd' || role === 'lider_doc') {
        bindLeader();
        const semesterInput = document.querySelector('#leader-sim-form input[name="semestre"]');
        if (semesterInput?.value) {
          await refreshLeaderCoverage(semesterInput.value);
        }
      } else if (role === 'auxiliar_sd' || role === 'auxiliar_doc') {
        bindAuxiliar();
      } else if (role === 'facultad') {
        bindFaculty();
      } else if (role === 'admisiones') {
        bindAdmissions();
      }
    } catch (error) {
      toast('error', error.details || error.message || 'No se pudo cargar el panel.');
    }
  };

  window.addEventListener('sds:catalog-changed', (event) => {
    const payload = event.detail || {};
    if (payload.tipo === 'progreso') {
      return;
    }
    scheduleRefresh();
  });

  if (document.readyState === 'loading') {
    window.addEventListener('DOMContentLoaded', boot, { once: true });
  } else {
    boot();
  }
})();
