import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api',
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

export function fetchPostDetail(postId) {
  return api.get(`/posts/${postId}`).then(res => res.data.data)
}

export function createPost(payload) {
  return api.post('/posts', payload).then(res => res.data.data)
}

export default api