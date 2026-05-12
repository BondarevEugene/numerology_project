import { Cpu, MessageSquare, Database, ShoppingCart, Globe, Shield } from 'lucide-react';

export const ALL_MODULES = [
  { id: 'rag', label: 'AI Knowledge Base', cat: 'ai', icon: Cpu, desc: 'Обучение на PDF/Docx документах' },
  { id: 'gpt4', label: 'GPT-4 Turbo', cat: 'ai', icon: MessageSquare, desc: 'Продвинутая логика рассуждений' },
  { id: 'shop', label: 'E-commerce Store', cat: 'shop', icon: ShoppingCart, desc: 'Витрина товаров и корзина' },
  { id: 'crm', label: 'CRM Sync', cat: 'core', icon: Database, desc: 'Интеграция с базой клиентов' },
  { id: 'proxy', label: 'Anti-Flood Shield', cat: 'core', icon: Shield, desc: 'Защита от спама и атак' },
  { id: 'web', label: 'Web Scraper', cat: 'logic', icon: Globe, desc: 'Парсинг данных из интернета' },
];