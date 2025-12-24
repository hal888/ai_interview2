import axios from 'axios'

// 创建axios实例
const apiClient = axios.create({
  baseURL: '/api',
  timeout: 120000
})

// 请求拦截器
apiClient.interceptors.request.use(
  config => {
    // 从localStorage获取令牌
    const token = localStorage.getItem('token')
    if (token) {
      // 添加Authorization头
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 响应拦截器
apiClient.interceptors.response.use(
  response => {
    return response
  },
  error => {
    if (error.response) {
      // 处理401认证失败
      if (error.response.status === 401) {
        // 清除本地存储的令牌
        localStorage.removeItem('token')
        localStorage.removeItem('userId')
        // 跳转到登录页面或提示用户重新登录
        alert('登录已过期，请重新登录')
        // 如果有路由，可以跳转到登录页
        // router.push('/login')
      }
    }
    return Promise.reject(error)
  }
)

export default apiClient