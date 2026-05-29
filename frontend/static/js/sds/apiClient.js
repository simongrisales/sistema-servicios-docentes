(function () {
  const getCsrfToken = () => {
    const el = document.querySelector('[name=csrfmiddlewaretoken]');
    return el ? el.value : '';
  };

  const getAccessToken = () => {
    return localStorage.getItem('sds_access_token') || '';
  };

  const buildHeaders = (extraHeaders) => {
    const headers = Object.assign(
      {
        'Content-Type': 'application/json',
      },
      extraHeaders || {}
    );

    const csrf = getCsrfToken();
    if (csrf && !headers['X-CSRFToken']) {
      headers['X-CSRFToken'] = csrf;
    }

    const access = getAccessToken();
    if (access && !headers.Authorization) {
      headers.Authorization = `Bearer ${access}`;
    }

    return headers;
  };

  const request = async ({
    url,
    method = 'GET',
    body = null,
    headers = {},
    parseJson = true,
    signal = undefined,
  }) => {
    const res = await fetch(url, {
      method,
      headers: buildHeaders(headers),
      body: body === null ? null : JSON.stringify(body),
      signal,
    });

    if (!res.ok) {
      let details = '';
      try {
        const data = await res.json();
        details = data?.detail || data?.message || JSON.stringify(data);
      } catch (e) {
        try {
          details = await res.text();
        } catch (_) {
          details = '';
        }
      }

      const err = new Error(`HTTP ${res.status} - ${details}`);
      err.status = res.status;
      err.details = details;
      throw err;
    }

    if (!parseJson) return null;

    return await res.json();
  };

  window.sds = window.sds || {};
  window.sds.apiClient = {
    get: (url, opts = {}) =>
      request({
        url,
        method: 'GET',
        ...opts,
      }),
    post: (url, body, opts = {}) =>
      request({
        url,
        method: 'POST',
        body,
        ...opts,
      }),
    put: (url, body, opts = {}) =>
      request({
        url,
        method: 'PUT',
        body,
        ...opts,
      }),
    del: (url, opts = {}) =>
      request({
        url,
        method: 'DELETE',
        ...opts,
      }),
  };
})();

