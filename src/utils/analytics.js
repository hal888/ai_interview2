/**
 * Analytics Utility
 * Handles integration with Google Analytics 4 and Baidu Tongji
 */

// Load Google Analytics script
const loadGA = (measurementId) => {
    if (!measurementId) return

    const script = document.createElement('script')
    script.async = true
    script.src = `https://www.googletagmanager.com/gtag/js?id=${measurementId}`
    document.head.appendChild(script)

    window.dataLayer = window.dataLayer || []
    function gtag() {
        window.dataLayer.push(arguments)
    }
    gtag('js', new Date())
    gtag('config', measurementId)

    window.gtag = gtag
}

// Load Baidu Tongji script
const loadBaidu = (key) => {
    if (!key) return

    window._hmt = window._hmt || []
    const script = document.createElement('script')
    script.src = `https://hm.baidu.com/hm.js?${key}`
    const s = document.getElementsByTagName('script')[0]
    s.parentNode.insertBefore(script, s)
}

// Initialize analytics
export const initAnalytics = () => {
    const gaId = import.meta.env.VITE_GA_MEASUREMENT_ID
    const baiduKey = import.meta.env.VITE_BAIDU_TONGJI_KEY

    if (gaId) {
        loadGA(gaId)
        console.log('Google Analytics initialized')
    }

    if (baiduKey) {
        loadBaidu(baiduKey)
        console.log('Baidu Tongji initialized')
    }
}

/**
 * Track an event
 * @param {string} eventName - The name of the event
 * @param {object} params - Event parameters
 */
export const trackEvent = (eventName, params = {}) => {
    // Google Analytics
    if (window.gtag) {
        window.gtag('event', eventName, params)
    }

    // Baidu Tongji
    if (window._hmt) {
        // Baidu Tongji uses _hmt.push(['_trackEvent', category, action, opt_label, opt_value])
        // We map our eventName to category/action for simplicity
        // Or use custom event API if available, but standard is _trackEvent
        // Here we map: category = 'general', action = eventName, label = JSON.stringify(params)
        const label = params ? JSON.stringify(params) : ''
        window._hmt.push(['_trackEvent', 'general', eventName, label])
    }

    // Console log for dev
    if (import.meta.env.DEV) {
        console.log(`[Analytics] Event: ${eventName}`, params)
    }
}
