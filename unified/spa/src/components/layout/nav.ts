export type NavItem = {
  label: string
  to: string
  icon: string // bootstrap-icons class name, e.g. "bi-speedometer2"
}

export const NAV_ITEMS: NavItem[] = [
  { label: 'Dashboard', to: '/', icon: 'bi-speedometer2' },
  { label: 'Tenants', to: '/tenants', icon: 'bi-buildings' },
  { label: 'Bots', to: '/bots', icon: 'bi-robot' },
  { label: 'Customers', to: '/customers', icon: 'bi-people' },
  { label: 'Conversations', to: '/conversations', icon: 'bi-chat-dots' },
  { label: 'Messages', to: '/messages', icon: 'bi-envelope' },
  { label: 'Users', to: '/users', icon: 'bi-person-badge' },
  { label: 'Billing', to: '/billings', icon: 'bi-credit-card' },
  { label: 'ACL Profiles', to: '/acl-profiles', icon: 'bi-shield-lock' },
]

