/**
 * 数据导出工具
 * 支持多种格式的数据导出和下载
 */

import { message } from 'ant-design-vue'
import dayjs from 'dayjs'

export type ExportFormat = 'json' | 'csv' | 'xml' | 'sql'

export interface ExportOptions {
  format: ExportFormat
  filename?: string
  formatOptions?: {
    csvDelimiter?: string
    jsonPrettyPrint?: boolean
    sqlTableName?: string
    xmlRootElement?: string
  }
}

/**
 * 数据导出服务
 */
export class ExportService {
  /**
   * 导出数据到文件
   */
  static async exportData(data: any[], options: ExportOptions): Promise<void> {
    try {
      if (!data || data.length === 0) {
        message.warning('没有数据可以导出')
        return
      }

      const { format, filename, formatOptions = {} } = options
      const timestamp = dayjs().format('YYYY-MM-DD_HH-mm-ss')
      const defaultFilename = `dataforge_export_${timestamp}`

      let content: string
      let mimeType: string
      let fileExtension: string

      switch (format) {
        case 'json':
          content = this.toJSON(data, formatOptions.jsonPrettyPrint)
          mimeType = 'application/json'
          fileExtension = 'json'
          break

        case 'csv':
          content = this.toCSV(data, formatOptions.csvDelimiter)
          mimeType = 'text/csv'
          fileExtension = 'csv'
          break

        case 'xml':
          content = this.toXML(data, formatOptions.xmlRootElement)
          mimeType = 'application/xml'
          fileExtension = 'xml'
          break

        case 'sql':
          content = this.toSQL(data, formatOptions.sqlTableName)
          mimeType = 'text/sql'
          fileExtension = 'sql'
          break

        default:
          throw new Error(`不支持的导出格式: ${format}`)
      }

      const finalFilename = `${filename || defaultFilename}.${fileExtension}`
      await this.downloadFile(content, finalFilename, mimeType)

      message.success(`数据已导出为 ${format.toUpperCase()} 格式`)
    } catch (error: any) {
      console.error('导出失败:', error)
      message.error(`导出失败: ${error.message}`)
    }
  }

  /**
   * 转换为JSON格式
   */
  private static toJSON(data: any[], prettyPrint = true): string {
    if (prettyPrint) {
      return JSON.stringify(data, null, 2)
    }
    return JSON.stringify(data)
  }

  /**
   * 转换为CSV格式
   */
  private static toCSV(data: any[], delimiter = ','): string {
    if (data.length === 0) return ''

    // 获取所有字段名
    const headers = Object.keys(data[0])
    const csvRows: string[] = []

    // 添加表头
    csvRows.push(headers.map(header => this.escapeCSVField(header)).join(delimiter))

    // 添加数据行
    for (const row of data) {
      const values = headers.map(header => {
        const value = row[header]
        return this.escapeCSVField(String(value || ''))
      })
      csvRows.push(values.join(delimiter))
    }

    return csvRows.join('\n')
  }

  /**
   * 转换为XML格式
   */
  private static toXML(data: any[], rootElement = 'data'): string {
    const xmlRows: string[] = []
    xmlRows.push('<?xml version="1.0" encoding="UTF-8"?>')
    xmlRows.push(`<${rootElement}>`)

    for (const [index, row] of data.entries()) {
      xmlRows.push(`  <record id="${index + 1}">`)

      for (const [key, value] of Object.entries(row)) {
        const escapedKey = this.escapeXMLTag(key)
        const escapedValue = this.escapeXMLContent(String(value || ''))
        xmlRows.push(`    <${escapedKey}>${escapedValue}</${escapedKey}>`)
      }

      xmlRows.push('  </record>')
    }

    xmlRows.push(`</${rootElement}>`)
    return xmlRows.join('\n')
  }

  /**
   * 转换为SQL格式
   */
  private static toSQL(data: any[], tableName = 'generated_data'): string {
    if (data.length === 0) return ''

    const headers = Object.keys(data[0])
    const sqlRows: string[] = []

    // 创建表结构
    sqlRows.push(`-- DataForge Generated Data Export`)
    sqlRows.push(`-- Generated at: ${dayjs().format('YYYY-MM-DD HH:mm:ss')}`)
    sqlRows.push(`-- Total records: ${data.length}`)
    sqlRows.push('')
    sqlRows.push(`DROP TABLE IF EXISTS \`${tableName}\`;`)
    sqlRows.push('')
    sqlRows.push(`CREATE TABLE \`${tableName}\` (`)

    const columnDefs = headers.map((header, index) => {
      const isLast = index === headers.length - 1
      return `  \`${header}\` TEXT${isLast ? '' : ','}`
    })
    sqlRows.push(...columnDefs)
    sqlRows.push(');')
    sqlRows.push('')

    // 插入数据
    sqlRows.push(`INSERT INTO \`${tableName}\` (${headers.map(h => `\`${h}\``).join(', ')}) VALUES`)

    const valueRows = data.map((row, index) => {
      const values = headers.map(header => {
        const value = row[header]
        return this.escapeSQLValue(value)
      })
      const isLast = index === data.length - 1
      return `  (${values.join(', ')})${isLast ? ';' : ','}`
    })

    sqlRows.push(...valueRows)
    return sqlRows.join('\n')
  }

  /**
   * CSV字段转义
   */
  private static escapeCSVField(field: string): string {
    if (field.includes(',') || field.includes('"') || field.includes('\n')) {
      return `"${field.replace(/"/g, '""')}"`
    }
    return field
  }

  /**
   * XML标签转义
   */
  private static escapeXMLTag(tag: string): string {
    return tag.replace(/[^a-zA-Z0-9_]/g, '_')
  }

  /**
   * XML内容转义
   */
  private static escapeXMLContent(content: string): string {
    return content
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&apos;')
  }

  /**
   * SQL值转义
   */
  private static escapeSQLValue(value: any): string {
    if (value === null || value === undefined) {
      return 'NULL'
    }

    if (typeof value === 'number') {
      return String(value)
    }

    if (typeof value === 'boolean') {
      return value ? '1' : '0'
    }

    // 字符串值需要转义单引号
    const stringValue = String(value)
    return `'${stringValue.replace(/'/g, "''")}'`
  }

  /**
   * 下载文件
   */
  private static async downloadFile(content: string, filename: string, mimeType: string): Promise<void> {
    try {
      // 创建Blob对象
      const blob = new Blob([content], { type: mimeType })

      // 创建下载链接
      const url = URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.download = filename

      // 添加到DOM并触发下载
      document.body.appendChild(link)
      link.click()

      // 清理
      document.body.removeChild(link)
      URL.revokeObjectURL(url)
    } catch (error) {
      throw new Error('文件下载失败')
    }
  }

  /**
   * 获取文件大小估算
   */
  static estimateFileSize(data: any[], format: ExportFormat): string {
    try {
      let content: string

      switch (format) {
        case 'json':
          content = this.toJSON(data, true)
          break
        case 'csv':
          content = this.toCSV(data)
          break
        case 'xml':
          content = this.toXML(data)
          break
        case 'sql':
          content = this.toSQL(data)
          break
        default:
          return '未知'
      }

      const bytes = new Blob([content]).size
      return this.formatBytes(bytes)
    } catch (error) {
      return '未知'
    }
  }

  /**
   * 格式化字节大小
   */
  private static formatBytes(bytes: number): string {
    if (bytes === 0) return '0 B'

    const sizes = ['B', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(1024))

    return `${(bytes / Math.pow(1024, i)).toFixed(1)} ${sizes[i]}`
  }

  /**
   * 验证导出数据
   */
  static validateExportData(data: any[]): { valid: boolean; message?: string } {
    if (!Array.isArray(data)) {
      return { valid: false, message: '数据格式无效，必须是数组' }
    }

    if (data.length === 0) {
      return { valid: false, message: '没有数据可以导出' }
    }

    // 检查数据一致性
    const firstRowKeys = Object.keys(data[0] || {})
    if (firstRowKeys.length === 0) {
      return { valid: false, message: '数据行为空' }
    }

    // 检查所有行是否有相同的字段结构
    for (const [index, row] of data.entries()) {
      const rowKeys = Object.keys(row)
      if (rowKeys.length !== firstRowKeys.length) {
        return {
          valid: false,
          message: `第 ${index + 1} 行字段数量不一致`
        }
      }
    }

    return { valid: true }
  }
}
