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
    // 为401错误添加特殊标志，以便组件识别
    if (error.response && error.response.status === 401) {
      error.isUnauthorized = true
      error.message = '请先登录'
    }
    return Promise.reject(error)
  }
)

export default apiClient