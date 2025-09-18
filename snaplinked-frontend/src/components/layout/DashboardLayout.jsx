import { useState } from 'react'
import { Link, useLocation, useNavigate } from 'react-router-dom'
import { Button } from '@/components/ui/button'
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu'
import { Badge } from '@/components/ui/badge'
import { useAuth } from '@/contexts/AuthContext'
import { useTheme } from '@/contexts/ThemeContext'
import {
  LayoutDashboard,
  Bot,
  Users,
  BarChart3,
  Settings,
  LogOut,
  Menu,
  X,
  Sun,
  Moon,
  Bell,
  CreditCard,
  User,
  HelpCircle,
} from 'lucide-react'

const navigation = [
  {
    name: 'Dashboard',
    href: '/dashboard',
    icon: LayoutDashboard,
  },
  {
    name: 'Automações',
    href: '/automations',
    icon: Bot,
  },
  {
    name: 'Contas LinkedIn',
    href: '/linkedin-accounts',
    icon: Users,
  },
  {
    name: 'Analytics',
    href: '/analytics',
    icon: BarChart3,
  },
  {
    name: 'Scripts',
    href: '/scripts',
    icon: ({ className }) => (
      <svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" />
      </svg>
    ),
  },
  {
    name: 'Configurações',
    href: '/settings',
    icon: Settings,
  },
]

export default function DashboardLayout({ children }) {
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const { user, logout } = useAuth()
  const { theme, setTheme } = useTheme()
  const location = useLocation()
  const navigate = useNavigate()

  const handleLogout = async () => {
    await logout()
    navigate('/login')
  }

  const getSubscriptionBadge = (plan) => {
    const badges = {
      free: { text: 'Gratuito', variant: 'secondary' },
      basic: { text: 'Básico', variant: 'default' },
      premium: { text: 'Premium', variant: 'default' },
      enterprise: { text: 'Enterprise', variant: 'default' },
    }
    return badges[plan] || badges.premium
  }

  const subscriptionBadge = getSubscriptionBadge(user?.subscription_plan)

  return (
    <div className="flex h-screen bg-gray-50 dark:bg-gray-900">
      {/* Mobile sidebar overlay */}
      {sidebarOpen && (
        <div 
          className="fixed inset-0 z-40 lg:hidden"
          onClick={() => setSidebarOpen(false)}
        >
          <div className="fixed inset-0 bg-gray-600 bg-opacity-75" />
        </div>
      )}

      {/* Sidebar */}
      <div className={`
        fixed inset-y-0 left-0 z-50 w-64 bg-white dark:bg-gray-800 shadow-lg transform transition-transform duration-300 ease-in-out lg:translate-x-0 lg:static lg:inset-0 lg:flex lg:flex-col
        ${sidebarOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'}
      `}>
        <div className="flex flex-col h-full">
          {/* Logo */}
          <div className="flex items-center justify-between h-16 px-6 border-b border-gray-200 dark:border-gray-700 flex-shrink-0">
            <Link to="/dashboard" className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-sm">SL</span>
              </div>
              <span className="text-xl font-bold text-gray-900 dark:text-white">SnapLinked</span>
            </Link>
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setSidebarOpen(false)}
              className="lg:hidden"
            >
              <X className="h-5 w-5" />
            </Button>
          </div>

          {/* User info */}
          <div className="p-6 border-b border-gray-200 dark:border-gray-700 flex-shrink-0">
            <div className="flex items-center space-x-3">
              <Avatar className="h-10 w-10">
                <AvatarImage src={user?.avatar_url} />
                <AvatarFallback className="bg-gradient-to-r from-blue-600 to-purple-600 text-white">
                  {user?.first_name?.[0] || 'D'}{user?.last_name?.[0] || 'U'}
                </AvatarFallback>
              </Avatar>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-gray-900 dark:text-white truncate">
                  {user?.first_name || 'Demo'} {user?.last_name || 'User'}
                </p>
                <div className="flex items-center space-x-2 mt-1">
                  <Badge variant={subscriptionBadge.variant} className="text-xs">
                    {subscriptionBadge.text}
                  </Badge>
                </div>
              </div>
            </div>
          </div>

          {/* Navigation */}
          <nav className="flex-1 px-4 py-6 space-y-2 overflow-y-auto">
            {navigation.map((item) => {
              const isActive = location.pathname === item.href
              return (
                <Link
                  key={item.name}
                  to={item.href}
                  className={`
                    flex items-center px-3 py-3 text-sm font-medium rounded-lg transition-all duration-200
                    ${isActive
                      ? 'bg-gradient-to-r from-blue-600 to-purple-600 text-white shadow-md'
                      : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 hover:text-gray-900 dark:hover:text-white'
                    }
                  `}
                  onClick={() => setSidebarOpen(false)}
                >
                  <item.icon className="mr-3 h-5 w-5 flex-shrink-0" />
                  <span className="truncate">{item.name}</span>
                </Link>
              )
            })}
          </nav>

          {/* Upgrade prompt for free users */}
          {user?.subscription_plan === 'free' && (
            <div className="p-4 m-4 bg-gradient-to-r from-blue-50 to-purple-50 dark:from-blue-900/20 dark:to-purple-900/20 rounded-lg border border-blue-200 dark:border-blue-800 flex-shrink-0">
              <h3 className="text-sm font-medium text-gray-900 dark:text-white mb-2">
                Upgrade para Premium
              </h3>
              <p className="text-xs text-gray-600 dark:text-gray-400 mb-3">
                Desbloqueie automações ilimitadas e recursos avançados.
              </p>
              <Link to="/pricing">
                <Button size="sm" className="w-full bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700">
                  Fazer Upgrade
                </Button>
              </Link>
            </div>
          )}
        </div>
      </div>

      {/* Main content area */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Top bar */}
        <header className="bg-white dark:bg-gray-800 shadow-sm border-b border-gray-200 dark:border-gray-700 flex-shrink-0">
          <div className="flex items-center justify-between h-16 px-6">
            <div className="flex items-center">
              <Button
                variant="ghost"
                size="sm"
                onClick={() => setSidebarOpen(true)}
                className="lg:hidden mr-2"
              >
                <Menu className="h-5 w-5" />
              </Button>
              
              <h1 className="text-lg font-semibold text-gray-900 dark:text-white">
                {navigation.find(item => item.href === location.pathname)?.name || 'Dashboard'}
              </h1>
            </div>

            <div className="flex items-center space-x-4">
              {/* Notifications */}
              <Button variant="ghost" size="sm" className="relative">
                <Bell className="h-5 w-5" />
                <span className="absolute -top-1 -right-1 h-3 w-3 bg-red-500 rounded-full text-xs"></span>
              </Button>

              {/* Theme toggle */}
              <Button
                variant="ghost"
                size="sm"
                onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')}
              >
                {theme === 'light' ? (
                  <Moon className="h-5 w-5" />
                ) : (
                  <Sun className="h-5 w-5" />
                )}
              </Button>

              {/* User menu */}
              <DropdownMenu>
                <DropdownMenuTrigger asChild>
                  <Button variant="ghost" className="relative h-8 w-8 rounded-full">
                    <Avatar className="h-8 w-8">
                      <AvatarImage src={user?.avatar_url} />
                      <AvatarFallback className="bg-gradient-to-r from-blue-600 to-purple-600 text-white text-xs">
                        {user?.first_name?.[0] || 'D'}{user?.last_name?.[0] || 'U'}
                      </AvatarFallback>
                    </Avatar>
                  </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent className="w-56" align="end" forceMount>
                  <DropdownMenuLabel className="font-normal">
                    <div className="flex flex-col space-y-1">
                      <p className="text-sm font-medium leading-none">
                        {user?.first_name || 'Demo'} {user?.last_name || 'User'}
                      </p>
                      <p className="text-xs leading-none text-muted-foreground">
                        {user?.email || 'demo@snaplinked.com'}
                      </p>
                    </div>
                  </DropdownMenuLabel>
                  <DropdownMenuSeparator />
                  <DropdownMenuItem asChild>
                    <Link to="/settings" className="cursor-pointer">
                      <User className="mr-2 h-4 w-4" />
                      Perfil
                    </Link>
                  </DropdownMenuItem>
                  <DropdownMenuItem asChild>
                    <Link to="/pricing" className="cursor-pointer">
                      <CreditCard className="mr-2 h-4 w-4" />
                      Faturamento
                    </Link>
                  </DropdownMenuItem>
                  <DropdownMenuItem>
                    <HelpCircle className="mr-2 h-4 w-4" />
                    Suporte
                  </DropdownMenuItem>
                  <DropdownMenuSeparator />
                  <DropdownMenuItem onClick={handleLogout} className="cursor-pointer">
                    <LogOut className="mr-2 h-4 w-4" />
                    Sair
                  </DropdownMenuItem>
                </DropdownMenuContent>
              </DropdownMenu>
            </div>
          </div>
        </header>

        {/* Page content */}
        <main className="flex-1 overflow-y-auto bg-gray-50 dark:bg-gray-900">
          <div className="p-6 max-w-7xl mx-auto">
            {children}
          </div>
        </main>
      </div>
    </div>
  )
}
