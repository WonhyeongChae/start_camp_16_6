import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '',
  headers: {
    'Content-Type': 'application/json'
  }
})

api.interceptors.response.use(
  response => response,
  error => {
    return Promise.reject(error.response?.data || error)
  }
)

export function fetchPlaces(params = {}) {
  return api.get('/places', { params }).then(res => res.data.data)
}

export function fetchPlaceDetail(contentId) {
  return api.get(`/places/${contentId}`).then(res => res.data.data)
}

export function fetchPosts(params = {}) {
  return api.get('/posts', { params }).then(res => res.data.data)
}

export default api