import { useState, useEffect } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Switch } from '@/components/ui/switch'
import { useAuth } from '@/contexts/AuthContext'
import { useToast } from '@/hooks/use-toast'
import {
  Check,
  ArrowLeft,
  Zap,
  Crown,
  Building,
  Star,
  Users,
  MessageSquare,
  Eye,
  BarChart3,
  Shield,
  Headphones,
  Code,
  Palette,
} from 'lucide-react'
import LoadingSpinner from '@/components/ui/loading-spinner'

export default function PricingPage() {
  const [isAnnual, setIsAnnual] = useState(false)
  const [loading, setLoading] = useState(false)
  const [plans, setPlans] = useState(null)
  const { user, apiCall } = useAuth()
  const { toast } = useToast()
  const navigate = useNavigate()

  useEffect(() => {
    loadPlans()
  }, [])

  const loadPlans = async () => {
    try {
      const response = await fetch('/api/payments/plans')
      const data = await response.json()
      
      if (data.success) {
        setPlans(data.plans)
      }
    } catch (error) {
      console.error('Failed to load plans:', error)
    }
  }

  const handleSubscribe = async (planId) => {
    if (!user) {
      navigate('/register')
      return
    }

    try {
      setLoading(true)
      
      const response = await apiCall('/payments/create-checkout-session', {
        method: 'POST',
        body: JSON.stringify({ plan: planId }),
      })

      if (response.success) {
        // Redirect to Stripe Checkout
        window.location.href = response.checkout_url
      } else {
        toast({
          title: 'Error',
          description: response.message || 'Failed to create checkout session',
          variant: 'destructive',
        })
      }
    } catch (error) {
      toast({
        title: 'Error',
        description: 'Failed to start checkout process',
        variant: 'destructive',
      })
    } finally {
      setLoading(false)
    }
  }

  const pricingPlans = [
    {
      id: 'free',
      name: 'Free',
      description: 'Perfect for getting started',
      price: { monthly: 0, annual: 0 },
      icon: Zap,
      color: 'text-gray-600',
      bgColor: 'bg-gray-50',
      popular: false,
      features: [
        '1 automation',
        '10 daily connections',
        '5 daily messages',
        '20 profile views',
        'Basic analytics',
        'Community support',
      ],
      limitations: [
        'Limited automation types',
        'Basic targeting options',
        'No bulk operations',
      ]
    },
    {
      id: 'basic',
      name: 'Basic',
      description: 'Great for individuals and small teams',
      price: { monthly: 29.99, annual: 299.99 },
      icon: Star,
      color: 'text-blue-600',
      bgColor: 'bg-blue-50',
      popular: false,
      features: [
        '5 automations',
        '50 daily connections',
        '25 daily messages',
        '100 profile views',
        'Advanced analytics',
        'Email support',
        'Custom message templates',
        'Basic targeting filters',
      ]
    },
    {
      id: 'premium',
      name: 'Premium',
      description: 'Best for growing businesses',
      price: { monthly: 79.99, annual: 799.99 },
      icon: Crown,
      color: 'text-purple-600',
      bgColor: 'bg-purple-50',
      popular: true,
      features: [
        '20 automations',
        '200 daily connections',
        '100 daily messages',
        '500 profile views',
        'Advanced analytics & reports',
        'Priority support',
        'Bulk operations',
        'Advanced targeting',
        'A/B testing',
        'Team collaboration',
        'Custom integrations',
      ]
    },
    {
      id: 'enterprise',
      name: 'Enterprise',
      description: 'For large organizations',
      price: { monthly: 199.99, annual: 1999.99 },
      icon: Building,
      color: 'text-green-600',
      bgColor: 'bg-green-50',
      popular: false,
      features: [
        '100 automations',
        '1000 daily connections',
        '500 daily messages',
        '2000 profile views',
        'Enterprise analytics',
        'Dedicated support',
        'White-label solution',
        'API access',
        'Custom integrations',
        'SSO authentication',
        'Advanced security',
        'Custom onboarding',
      ]
    }
  ]

  const featureIcons = {
    'automations': Bot,
    'connections': Users,
    'messages': MessageSquare,
    'views': Eye,
    'analytics': BarChart3,
    'support': Headphones,
    'security': Shield,
    'api': Code,
    'white-label': Palette,
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      {/* Navigation */}
      <nav className="border-b bg-white/80 backdrop-blur-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <Link to="/" className="flex items-center space-x-2">
              <ArrowLeft className="w-4 h-4 mr-2" />
              <div className="w-8 h-8 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-sm">SL</span>
              </div>
              <span className="text-xl font-bold text-gray-900">SnapLinked</span>
            </Link>
            
            <div className="flex items-center space-x-4">
              {user ? (
                <Link to="/dashboard">
                  <Button variant="outline">Dashboard</Button>
                </Link>
              ) : (
                <>
                  <Link to="/login">
                    <Button variant="ghost">Sign In</Button>
                  </Link>
                  <Link to="/register">
                    <Button className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700">
                      Get Started
                    </Button>
                  </Link>
                </>
              )}
            </div>
          </div>
        </div>
      </nav>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
            Choose Your Plan
          </h1>
          <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
            Scale your LinkedIn automation with the perfect plan for your needs. 
            Start free and upgrade as you grow.
          </p>
          
          {/* Billing Toggle */}
          <div className="flex items-center justify-center space-x-4 mb-8">
            <span className={`text-sm ${!isAnnual ? 'text-gray-900 font-medium' : 'text-gray-500'}`}>
              Monthly
            </span>
            <Switch
              checked={isAnnual}
              onCheckedChange={setIsAnnual}
              className="data-[state=checked]:bg-gradient-to-r data-[state=checked]:from-blue-600 data-[state=checked]:to-purple-600"
            />
            <span className={`text-sm ${isAnnual ? 'text-gray-900 font-medium' : 'text-gray-500'}`}>
              Annual
            </span>
            <Badge className="bg-green-100 text-green-800 hover:bg-green-100">
              Save 17%
            </Badge>
          </div>
        </div>

        {/* Pricing Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 mb-16">
          {pricingPlans.map((plan) => {
            const Icon = plan.icon
            const price = isAnnual ? plan.price.annual : plan.price.monthly
            const isCurrentPlan = user?.subscription_plan === plan.id
            
            return (
              <Card 
                key={plan.id} 
                className={`relative border-2 transition-all duration-300 hover:shadow-xl ${
                  plan.popular 
                    ? 'border-purple-200 shadow-lg scale-105' 
                    : 'border-gray-200 hover:border-gray-300'
                }`}
              >
                {plan.popular && (
                  <div className="absolute -top-3 left-1/2 transform -translate-x-1/2">
                    <Badge className="bg-gradient-to-r from-blue-600 to-purple-600 text-white px-4 py-1">
                      Most Popular
                    </Badge>
                  </div>
                )}
                
                <CardHeader className="text-center pb-4">
                  <div className={`w-12 h-12 ${plan.bgColor} rounded-lg flex items-center justify-center mx-auto mb-4`}>
                    <Icon className={`w-6 h-6 ${plan.color}`} />
                  </div>
                  <CardTitle className="text-xl font-bold">{plan.name}</CardTitle>
                  <CardDescription className="text-gray-600">
                    {plan.description}
                  </CardDescription>
                  
                  <div className="mt-4">
                    <div className="flex items-baseline justify-center">
                      <span className="text-4xl font-bold text-gray-900">
                        ${price === 0 ? '0' : price.toFixed(0)}
                      </span>
                      {price > 0 && (
                        <span className="text-gray-500 ml-1">
                          /{isAnnual ? 'year' : 'month'}
                        </span>
                      )}
                    </div>
                    {isAnnual && price > 0 && (
                      <p className="text-sm text-gray-500 mt-1">
                        ${(price / 12).toFixed(2)}/month billed annually
                      </p>
                    )}
                  </div>
                </CardHeader>
                
                <CardContent>
                  <div className="space-y-3 mb-6">
                    {plan.features.map((feature, index) => (
                      <div key={index} className="flex items-center">
                        <Check className="w-4 h-4 text-green-500 mr-3 flex-shrink-0" />
                        <span className="text-sm text-gray-700">{feature}</span>
                      </div>
                    ))}
                  </div>
                  
                  {plan.limitations && (
                    <div className="space-y-2 mb-6 pt-4 border-t border-gray-100">
                      {plan.limitations.map((limitation, index) => (
                        <div key={index} className="flex items-center">
                          <div className="w-4 h-4 mr-3 flex-shrink-0">
                            <div className="w-1 h-1 bg-gray-400 rounded-full mx-auto"></div>
                          </div>
                          <span className="text-xs text-gray-500">{limitation}</span>
                        </div>
                      ))}
                    </div>
                  )}
                  
                  <Button
                    className={`w-full ${
                      plan.popular
                        ? 'bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700'
                        : plan.id === 'free'
                        ? 'bg-gray-600 hover:bg-gray-700'
                        : 'bg-gray-900 hover:bg-gray-800'
                    }`}
                    onClick={() => handleSubscribe(plan.id)}
                    disabled={loading || isCurrentPlan || plan.id === 'free'}
                  >
                    {loading ? (
                      <LoadingSpinner size="sm" className="mr-2" />
                    ) : null}
                    {isCurrentPlan 
                      ? 'Current Plan' 
                      : plan.id === 'free' 
                      ? 'Get Started Free' 
                      : `Subscribe to ${plan.name}`
                    }
                  </Button>
                  
                  {plan.id === 'enterprise' && (
                    <p className="text-xs text-center text-gray-500 mt-2">
                      Contact sales for custom pricing
                    </p>
                  )}
                </CardContent>
              </Card>
            )
          })}
        </div>

        {/* Feature Comparison */}
        <div className="bg-white rounded-lg shadow-lg p-8 mb-16">
          <h2 className="text-2xl font-bold text-center mb-8">Feature Comparison</h2>
          
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b">
                  <th className="text-left py-4 px-4">Features</th>
                  <th className="text-center py-4 px-4">Free</th>
                  <th className="text-center py-4 px-4">Basic</th>
                  <th className="text-center py-4 px-4">Premium</th>
                  <th className="text-center py-4 px-4">Enterprise</th>
                </tr>
              </thead>
              <tbody>
                {[
                  { feature: 'Automations', values: ['1', '5', '20', '100'] },
                  { feature: 'Daily Connections', values: ['10', '50', '200', '1000'] },
                  { feature: 'Daily Messages', values: ['5', '25', '100', '500'] },
                  { feature: 'Profile Views', values: ['20', '100', '500', '2000'] },
                  { feature: 'Analytics', values: ['Basic', 'Advanced', 'Advanced', 'Enterprise'] },
                  { feature: 'Support', values: ['Community', 'Email', 'Priority', 'Dedicated'] },
                  { feature: 'Bulk Operations', values: ['✗', '✗', '✓', '✓'] },
                  { feature: 'API Access', values: ['✗', '✗', '✗', '✓'] },
                  { feature: 'White Label', values: ['✗', '✗', '✗', '✓'] },
                ].map((row, index) => (
                  <tr key={index} className="border-b border-gray-100">
                    <td className="py-4 px-4 font-medium">{row.feature}</td>
                    {row.values.map((value, valueIndex) => (
                      <td key={valueIndex} className="py-4 px-4 text-center">
                        {value === '✓' ? (
                          <Check className="w-5 h-5 text-green-500 mx-auto" />
                        ) : value === '✗' ? (
                          <span className="text-gray-400">—</span>
                        ) : (
                          value
                        )}
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* FAQ Section */}
        <div className="text-center">
          <h2 className="text-2xl font-bold mb-8">Frequently Asked Questions</h2>
          
          <div className="grid md:grid-cols-2 gap-8 max-w-4xl mx-auto">
            {[
              {
                question: 'Can I change plans anytime?',
                answer: 'Yes, you can upgrade or downgrade your plan at any time. Changes take effect immediately.'
              },
              {
                question: 'Is there a free trial?',
                answer: 'Yes! All paid plans come with a 14-day free trial. No credit card required to start.'
              },
              {
                question: 'What happens if I exceed my limits?',
                answer: 'Your automations will pause until the next billing cycle or you can upgrade your plan.'
              },
              {
                question: 'Is my LinkedIn account safe?',
                answer: 'Absolutely. We use human-like behavior patterns and respect LinkedIn\'s terms of service.'
              }
            ].map((faq, index) => (
              <div key={index} className="text-left">
                <h3 className="font-semibold mb-2">{faq.question}</h3>
                <p className="text-gray-600 text-sm">{faq.answer}</p>
              </div>
            ))}
          </div>
          
          <div className="mt-12">
            <p className="text-gray-600 mb-4">
              Still have questions? We're here to help.
            </p>
            <Button variant="outline">
              Contact Support
            </Button>
          </div>
        </div>
      </div>
    </div>
  )
}
