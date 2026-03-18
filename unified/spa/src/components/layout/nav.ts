export type NavItem = {
  label: string
  to: string
}

export const NAV_ITEMS: NavItem[] = [
  { label: 'Dashboard', to: '/' },
  { label: 'Tenants', to: '/tenants' },
  { label: 'Bots', to: '/bots' },
  { label: 'Customers', to: '/customers' },
  { label: 'Conversations', to: '/conversations' },
  { label: 'Messages', to: '/messages' },
  { label: 'Users', to: '/users' },
  { label: 'Billing', to: '/billings' },
  { label: 'ACL Profiles', to: '/acl-profiles' },
]

