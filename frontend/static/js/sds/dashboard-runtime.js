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
    aulasAdmin: [],
    grupos: [],
    docentes: [],
    cursos: [],
    facultades: [],
    programas: [],
    bloques: [],
    reservas: [],
    parametros: [],
    admissionsDraft: [],
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

  const uniqueBy = (items, keyFn) => {
    const seen = new Map();
    for (const item of items) {
      const key = keyFn(item);
      if (!key || seen.has(key)) {
        continue;
      }
      seen.set(key, item);
    }
    return Array.from(seen.values());
  };

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
    const [
      roles,
      users,
      aulas,
      aulasAdmin,
      grupos,
      docentes,
      cursos,
      facultades,
      programas,
      bloques,
      reservas,
      parametros,
    ] = await Promise.all([
      fetchJson('/api/usuarios/catalogo-roles/').catch(() => []),
      fetchJson('/api/usuarios/lista/').catch(() => []),
      fetchJson('/api/academico/aulas/').catch(() => []),
      fetchJson('/api/academico/aulas/buscar/').catch(() => []),
      fetchJson('/api/academico/aulas/grupos/').catch(() => []),
      fetchJson('/api/academico/aulas/docentes/').catch(() => []),
      fetchJson('/api/academico/aulas/cursos/').catch(() => []),
      fetchJson('/api/academico/aulas/facultades/').catch(() => []),
      fetchJson('/api/academico/aulas/programas/').catch(() => []),
      fetchJson('/api/academico/aulas/bloques/').catch(() => []),
      fetchJson('/api/reservas/').catch(() => []),
      fetchJson('/api/parametros/').catch(() => []),
    ]);

    state.roles = roles;
    state.users = users;
    state.aulas = aulas;
    state.aulasAdmin = aulasAdmin;
    state.grupos = grupos;
    state.docentes = docentes;
    state.cursos = cursos;
    state.facultades = facultades;
    state.programas = programas;
    state.bloques = bloques;
    state.reservas = reservas;
    state.parametros = parametros;
  };

  const getAdmissionsFacultades = () =>
    state.facultades.map((item) => ({
      id: item.id,
      codigo: item.codigo,
      nombre: item.nombre,
      programas: Number(item.programas || 0),
    }));

  const getAdmissionsProgramas = (facultadId) =>
    state.programas
      .filter((item) => String(item.facultad_id) === String(facultadId))
      .map((item) => ({
        id: item.id,
        codigo: item.codigo,
        nombre: item.nombre,
        facultad_id: item.facultad_id,
        facultad_nombre: item.facultad_nombre,
      }));

  const getAdmissionsCursos = (programaId) =>
    state.cursos.filter((item) => String(item.programa_id) === String(programaId));

  const getSelectedOption = (selectId) =>
    document.getElementById(selectId)?.value || '';

  const setSelectedOption = (selectId, value) => {
    const select = document.getElementById(selectId);
    if (!select || !value) {
      return;
    }
    if (Array.from(select.options).some((option) => option.value === String(value))) {
      select.value = String(value);
    }
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
    const adminQuery = normalizeText(document.getElementById('admin-aula-search')?.value || '');
    const aulasAdmin = adminQuery
      ? state.aulasAdmin.filter((aula) => {
          const haystack = normalizeText(
            [aula.nombre, aula.capacidad, aula.tipo, aula.disponible ? 'disponible' : 'ocupada']
              .filter(Boolean)
              .join(' ')
          );
          return haystack.includes(adminQuery);
        })
      : state.aulasAdmin;

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

    const aulasAdminRows = aulasAdmin
      .map(
        (aula) =>
          `<tr>
            <td>${esc(aula.nombre)}</td>
            <td>${esc(aula.capacidad)}</td>
            <td>${esc(aula.tipo)}</td>
            <td><span class="badge ${aula.disponible ? 'badge-success' : 'badge-warning'}">${aula.disponible ? 'Disponible' : 'Ocupada'}</span></td>
            <td>
              <button class="btn btn-ghost" type="button" data-aula-toggle="${esc(aula.id)}">
                ${aula.disponible ? 'Marcar ocupada' : 'Marcar disponible'}
              </button>
            </td>
          </tr>`
      )
      .join('');

    renderTable(
      'admin-aulas-body',
      aulasAdminRows || `<tr><td colspan="5">${esc(adminQuery ? 'No hay aulas que coincidan con el filtro' : 'No hay aulas registradas')}</td></tr>`
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
    const aulaSearch = document.getElementById('admin-aula-search');
    const aulaBody = document.getElementById('admin-aulas-body');

    aulaSearch?.addEventListener('input', () => {
      renderAdmin();
    });

    aulaBody?.addEventListener('click', async (evt) => {
      const button = evt.target.closest('[data-aula-toggle]');
      if (!button) {
        return;
      }
      const aulaId = button.getAttribute('data-aula-toggle');
      const aula = state.aulasAdmin.find((item) => String(item.id) === String(aulaId));
      if (!aula) {
        return;
      }
      try {
        await api().patch(`/api/academico/aulas/${aulaId}/estado/`, {
          disponible: !aula.disponible,
        });
        toast('success', 'Estado del aula actualizado.');
        await refreshCurrentPanel();
      } catch (error) {
        toast('error', error.details || 'No se pudo actualizar el estado del aula.');
      }
    });

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
      const semesterValue = formDataObject(simForm).semestre;
      if (!semesterValue) {
        showStatus('leader-sim-status', 'Debes indicar un semestre para ejecutar la asignacion.', 'error');
        return;
      }
      const confirmed = window.confirm(
        `Vas a ejecutar la asignacion automatica completa para ${semesterValue}. ¿Deseas continuar?`
      );
      if (!confirmed) {
        return;
      }
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

  const renderAdmissionsSelectors = () => {
    const facultySelect = document.getElementById('admissions-facultad-select');
    const programSelect = document.getElementById('admissions-programa-select');
    const courseSelect = document.getElementById('admissions-curso-select');
    const docenteSelect = document.getElementById('admissions-docente-select');
    if (!facultySelect || !programSelect || !courseSelect || !docenteSelect) {
      return;
    }

    const currentFaculty = facultySelect.value;
    const currentProgram = programSelect.value;
    const currentCourse = courseSelect.value;

    const faculties = getAdmissionsFacultades();
    renderOptions('admissions-facultad-select', faculties, {
      placeholder: 'Selecciona una facultad',
      valueKey: 'id',
      labelFn: (item) => (item.codigo ? `${item.nombre} (${item.codigo})` : item.nombre),
    });
    if (currentFaculty) {
      setSelectedOption('admissions-facultad-select', currentFaculty);
    } else if (faculties[0]) {
      setSelectedOption('admissions-facultad-select', faculties[0].id);
    }

    const activeFaculty = getSelectedOption('admissions-facultad-select');
    const programs = getAdmissionsProgramas(activeFaculty);
    renderOptions('admissions-programa-select', programs, {
      placeholder: 'Selecciona un programa',
      valueKey: 'id',
      labelFn: (item) => (item.codigo ? `${item.nombre} (${item.codigo})` : item.nombre),
    });
    if (currentProgram && programs.some((item) => String(item.id) === String(currentProgram))) {
      setSelectedOption('admissions-programa-select', currentProgram);
    } else if (programs[0]) {
      setSelectedOption('admissions-programa-select', programs[0].id);
    }

    const activeProgram = getSelectedOption('admissions-programa-select');
    const courses = getAdmissionsCursos(activeProgram);
    renderOptions('admissions-curso-select', courses, {
      placeholder: 'Selecciona un curso',
      valueKey: 'id',
      labelFn: (item) => `${item.codigo} - ${item.nombre}`,
    });
    if (currentCourse && courses.some((item) => String(item.id) === String(currentCourse))) {
      setSelectedOption('admissions-curso-select', currentCourse);
    } else if (courses[0]) {
      setSelectedOption('admissions-curso-select', courses[0].id);
    }

    renderOptions('admissions-docente-select', state.docentes, {
      placeholder: 'Selecciona un docente',
      valueKey: 'id',
      labelFn: (item) => `${item.nombre} - ${item.email}`,
    });
  };

  const renderAdmissionsQueue = () => {
    const queueBody = document.getElementById('admissions-queue-body');
    const summaryBody = document.getElementById('admissions-summary-body');
    const queueCount = document.getElementById('admissions-queue-count');
    const queueTotal = document.getElementById('admissions-queue-total');

    const totalStudents = state.admissionsDraft.reduce(
      (acc, item) => acc + Number(item.num_estudiantes || 0),
      0
    );

    if (queueCount) {
      queueCount.textContent = `${state.admissionsDraft.length} grupos`;
    }
    if (queueTotal) {
      queueTotal.textContent = `${totalStudents} estudiantes`;
    }

    if (queueBody) {
      queueBody.innerHTML = state.admissionsDraft.length
        ? state.admissionsDraft
            .map(
              (item, index) =>
                `<tr>
                  <td>${esc(item.facultad_nombre)}</td>
                  <td>${esc(item.programa_nombre)}</td>
                  <td>${esc(item.curso_nombre)}</td>
                  <td>${esc(item.docente_nombre)}</td>
                  <td>${esc(item.codigo)}</td>
                  <td>${esc(item.num_estudiantes)}</td>
                  <td>
                    <button class="btn btn-ghost" type="button" data-admissions-remove="${index}">Quitar</button>
                  </td>
                </tr>`
            )
            .join('')
        : '<tr><td colspan="7">No hay grupos en el lote</td></tr>';
    }

    if (summaryBody) {
      const summary = new Map();
      for (const item of state.admissionsDraft) {
        const key = `${item.facultad_nombre}::${item.programa_nombre}`;
        const current = summary.get(key) || {
          facultad_nombre: item.facultad_nombre,
          programa_nombre: item.programa_nombre,
          grupos: 0,
          estudiantes: 0,
        };
        current.grupos += 1;
        current.estudiantes += Number(item.num_estudiantes || 0);
        summary.set(key, current);
      }

      summaryBody.innerHTML = summary.size
        ? Array.from(summary.values())
            .map(
              (item) =>
                `<tr><td>${esc(item.facultad_nombre)}</td><td>${esc(item.programa_nombre)}</td><td>${esc(item.grupos)}</td><td>${esc(item.estudiantes)}</td></tr>`
            )
            .join('')
        : '<tr><td colspan="4">Sin resumen disponible</td></tr>';
    }

    document.querySelectorAll('[data-admissions-remove]').forEach((button) => {
      button.addEventListener('click', () => {
        const index = Number.parseInt(button.getAttribute('data-admissions-remove') || '-1', 10);
        if (Number.isNaN(index) || index < 0) {
          return;
        }
        state.admissionsDraft.splice(index, 1);
        renderAdmissionsQueue();
      });
    });
  };

  const renderAdmissions = () => {
    renderAdmissionsSelectors();
    renderAdmissionsQueue();

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
    const addRowButton = document.getElementById('admissions-add-row');
    const clearFormButton = document.getElementById('admissions-clear-form');
    const facultySelect = document.getElementById('admissions-facultad-select');
    const programSelect = document.getElementById('admissions-programa-select');

    const processQueue = async () => {
      if (!state.admissionsDraft.length) {
        showStatus('admissions-bulk-status', 'Agrega al menos un grupo al lote antes de procesar.', 'error');
        return;
      }

      let successCount = 0;
      let errorCount = 0;
      const remainingDraft = [];

      for (const item of state.admissionsDraft) {
        try {
          await postJson('/api/academico/aulas/grupos/', {
            curso_id: item.curso_id,
            docente_id: item.docente_id,
            codigo: item.codigo,
            num_estudiantes: Number(item.num_estudiantes),
            semestre: item.semestre,
          });
          successCount += 1;
        } catch (error) {
          errorCount += 1;
          remainingDraft.push(item);
        }
      }

      const total = state.admissionsDraft.length;
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
      state.admissionsDraft = remainingDraft;
      renderAdmissionsQueue();
      if (state.admissionsDraft.length === 0) {
        form?.reset();
      }
      renderAdmissionsSelectors();
      await refreshCurrentPanel();
    };

    facultySelect?.addEventListener('change', () => {
      renderAdmissionsSelectors();
    });

    programSelect?.addEventListener('change', () => {
      renderAdmissionsSelectors();
    });

    addRowButton?.addEventListener('click', () => {
      const data = formDataObject(form);
      const curso = state.cursos.find((item) => String(item.id) === String(data.curso_id));
      const docente = state.docentes.find((item) => String(item.id) === String(data.docente_id));
      const facultad = getAdmissionsFacultades().find(
        (item) => item.id === getSelectedOption('admissions-facultad-select')
      );
      const programa = getAdmissionsProgramas(getSelectedOption('admissions-facultad-select')).find(
        (item) => String(item.id) === String(getSelectedOption('admissions-programa-select'))
      );

      if (
        !curso ||
        !docente ||
        !facultad ||
        !programa ||
        String(curso.programa_id) !== String(programa.id) ||
        !data.codigo ||
        !data.num_estudiantes ||
        !data.semestre
      ) {
        showStatus('admissions-bulk-status', 'Completa la facultad, el programa, el curso, el docente y los datos del grupo.', 'error');
        return;
      }

      state.admissionsDraft.push({
        facultad_id: String(facultad.id),
        facultad_nombre: facultad.nombre,
        programa_id: String(programa.id),
        programa_nombre: programa.nombre,
        curso_id: String(curso.id),
        curso_nombre: `${curso.codigo} - ${curso.nombre}`,
        docente_id: String(docente.id),
        docente_nombre: `${docente.nombre} - ${docente.email}`,
        codigo: data.codigo,
        num_estudiantes: Number(data.num_estudiantes),
        semestre: data.semestre,
      });
      renderAdmissionsQueue();
      showStatus('admissions-bulk-status', 'Grupo agregado al lote. Puedes seguir sumando mas registros o procesarlo.', 'success');
    });

    clearFormButton?.addEventListener('click', () => {
      form?.reset();
      renderAdmissionsSelectors();
      showStatus('admissions-bulk-status', 'Formulario limpiado.', 'info');
    });

    form?.addEventListener('submit', async (evt) => {
      evt.preventDefault();
      await processQueue();
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
