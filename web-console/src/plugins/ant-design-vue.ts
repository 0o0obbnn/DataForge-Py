/**
 * Ant Design Vue 插件配置
 * 实现全量引入和主题定制
 */

import type { App } from 'vue'
import Antd, { message, notification, Modal } from 'ant-design-vue'
import 'ant-design-vue/dist/reset.css'
import '../assets/styles/theme.less'

// 主题配置 - 科技感·未来风深色主题
const themeConfig = {
  token: {
    // 主色调
    colorPrimary: '#8E5DFF',
    colorSuccess: '#00E676',
    colorWarning: '#FFC107',
    colorError: '#FF5252',

    // 背景色
    colorBgBase: '#1A1A2E',
    colorBgContainer: '#282845',
    colorBgElevated: '#282845',
    colorBgLayout: '#1A1A2E',

    // 文本色
    colorTextBase: '#E0E0E0',
    colorText: '#E0E0E0',
    colorTextSecondary: '#B0B0B0',
    colorTextTertiary: '#4A4A6D',

    // 边框色
    colorBorder: '#4A4A6D',
    colorBorderSecondary: '#4A4A6D',

    // 圆角
    borderRadius: 8,
    borderRadiusLG: 12,
    borderRadiusSM: 4,

    // 字体
    fontFamily: 'Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
    fontSize: 14,
    fontSizeLG: 16,
    fontSizeSM: 12,

    // 阴影
    boxShadow: '0 2px 8px rgba(0, 0, 0, 0.2)',
    boxShadowSecondary: '0 1px 4px rgba(0, 0, 0, 0.1)',

    // 间距
    padding: 16,
    paddingLG: 24,
    paddingSM: 8,
    margin: 16,
    marginLG: 24,
    marginSM: 8
  },
  components: {
    Button: {
      borderRadius: 4,
      controlHeight: 36,
      fontWeight: 500
    },
    Input: {
      borderRadius: 4,
      controlHeight: 36,
      colorBgContainer: '#282845',
      colorBorder: '#4A4A6D',
      colorText: '#E0E0E0',
      colorTextPlaceholder: '#B0B0B0'
    },
    Card: {
      borderRadius: 8,
      colorBgContainer: '#282845',
      colorBorder: '#4A4A6D',
      boxShadow: '0 2px 8px rgba(0, 0, 0, 0.2)'
    },
    Menu: {
      colorBgContainer: '#1A1A2E',
      colorItemBg: 'transparent',
      colorItemBgSelected: '#282845',
      colorItemBgHover: 'rgba(142, 93, 255, 0.1)',
      colorItemText: '#B0B0B0',
      colorItemTextSelected: '#E0E0E0',
      colorItemTextHover: '#E0E0E0'
    },
    Table: {
      colorBgContainer: '#282845',
      colorBorderSecondary: '#4A4A6D',
      colorText: '#E0E0E0',
      colorTextHeading: '#E0E0E0'
    },
    Modal: {
      colorBgElevated: '#282845',
      colorText: '#E0E0E0',
      colorTextHeading: '#E0E0E0'
    }
  }
}

export function setupAntDesignVue(app: App) {
  // 全量引入 Ant Design Vue
  app.use(Antd, {
    theme: themeConfig
  })

  // 全局配置
  message.config({
    top: '20px',
    duration: 3,
    maxCount: 3,
  })

  notification.config({
    placement: 'topRight',
    duration: 4.5,
    top: '24px'
  })

  Modal.config({
    centered: true,
  })

  // 挂载到全局
  app.config.globalProperties.$message = message
  app.config.globalProperties.$notification = notification
  app.config.globalProperties.$modal = Modal
}

export default setupAntDesignVue
