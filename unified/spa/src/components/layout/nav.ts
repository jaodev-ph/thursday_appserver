export type NavItem = {
  label: string
  to: string
  icon: string // bootstrap-icons class name, e.g. "bi-speedometer2"
}

export const NAV_ITEMS: NavItem[] = [
  { label: 'Dashboard', to: '/admin/dashboard', icon: 'bi-speedometer2' },
  { label: 'Tenants', to: '/admin/tenants', icon: 'bi-buildings' },
  { label: 'Bots', to: '/admin/bots', icon: 'bi-robot' },
  { label: 'Customers', to: '/admin/customers', icon: 'bi-people' },
  { label: 'Conversations', to: '/admin/conversations', icon: 'bi-chat-dots' },
  { label: 'Messages', to: '/admin/messages', icon: 'bi-envelope' },
  { label: 'Users', to: '/admin/users', icon: 'bi-person-badge' },
  { label: 'Billing', to: '/admin/billings', icon: 'bi-credit-card' },
  { label: 'ACL Profiles', to: '/admin/acl-profiles', icon: 'bi-shield-lock' },
]

