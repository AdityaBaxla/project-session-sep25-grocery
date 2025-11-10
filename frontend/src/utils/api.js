// Use environment variable when available, fall back to localhost for development
const baseURL = "http://localhost:5000/api";

const api = {
  async request(endpoint, options = {}) {
    // ensure endpoint starts with a slash
    const path = endpoint.startsWith("/") ? endpoint : `/${endpoint}`;
    const url = `${baseURL.replace(/\/$/, "")}${path}`;
    const token = localStorage.getItem("access_token");

    const headers = {
      "Content-Type": "application/json",
      ...options.headers,
    };

    if (token) {
      headers["Authentication-Token"] = token;
    }

    const config = {
      ...options,
      headers,
    };

    try {
      const response = await fetch(url, config);

      if (response.status === 401) {
        alert("Please login first");
        // router.push('/login');
        throw new Error("Unauthorized");
      }

      if (!response.ok) {
        // try to read error body for better message
        let bodyText = null;
        try {
          bodyText = await response.text();
        } catch (e) {
          /* ignore */
        }
        const message = bodyText
          ? `${response.status} - ${bodyText}`
          : `HTTP error! status: ${response.status}`;
        const err = new Error(message);
        err.status = response.status;
        throw err;
      }

      // 204 No Content or empty body
      if (response.status === 204) return null;
      const text = await response.text();
      if (!text) return null;
      try {
        return JSON.parse(text);
      } catch (e) {
        // not JSON, return raw text
        return text;
      }
    } catch (error) {
      return Promise.reject(error);
    }
  },

  get(endpoint, options = {}) {
    return this.request(endpoint, { ...options, method: "GET" });
  },

  post(endpoint, data, options = {}) {
    return this.request(endpoint, {
      ...options,
      method: "POST",
      body: JSON.stringify(data),
    });
  },

  put(endpoint, data, options = {}) {
    return this.request(endpoint, {
      ...options,
      method: "PUT",
      body: JSON.stringify(data),
    });
  },
  patch(endpoint, data, options = {}) {
    return this.request(endpoint, {
      ...options,
      method: "PATCH",
      body: JSON.stringify(data),
    });
  },

  delete(endpoint, options = {}) {
    return this.request(endpoint, { ...options, method: "DELETE" });
  },
};

export default api;
