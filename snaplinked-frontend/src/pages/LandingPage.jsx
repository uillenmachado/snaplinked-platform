import { Link } from 'react-router-dom'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { 
  ArrowRight, 
  CheckCircle, 
  Users, 
  MessageSquare, 
  Eye, 
  BarChart3,
  Shield,
  Zap,
  Clock,
  Target,
  Linkedin,
  Play
} from 'lucide-react'

export default function LandingPage() {
  const features = [
    {
      icon: Users,
      title: 'Conexões Automatizadas',
      description: 'Envie solicitações de conexão personalizadas para prospects direcionados automaticamente.',
    },
    {
      icon: MessageSquare,
      title: 'Mensagens Inteligentes',
      description: 'Faça follow-up com mensagens personalizadas para construir relacionamentos significativos.',
    },
    {
      icon: Eye,
      title: 'Visualização de Perfis',
      description: 'Aumente sua visibilidade visualizando automaticamente perfis relevantes.',
    },
    {
      icon: BarChart3,
      title: 'Analytics Avançados',
      description: 'Acompanhe o desempenho do seu outreach com analytics detalhados e insights.',
    },
    {
      icon: Shield,
      title: 'Seguro e Compatível',
      description: 'Padrões de comportamento humano para manter sua conta LinkedIn segura.',
    },
    {
      icon: Zap,
      title: 'Super Rápido',
      description: 'Configure suas automações em minutos, não horas.',
    },
  ]

  const benefits = [
    'Economize 10+ horas por semana em outreach no LinkedIn',
    'Aumente a taxa de aceitação de conexões em 300%',
    'Gere 5x mais leads qualificados',
    'Escale o crescimento da sua rede automaticamente',
    'Mantenha comunicação autêntica e personalizada',
    'Obtenha insights detalhados de performance'
  ]

  const testimonials = [
    {
      name: 'Sarah Johnson',
      role: 'Diretora de Vendas na TechCorp',
      content: 'O SnapLinked transformou nossa geração de leads. Vimos um aumento de 400% em prospects qualificados.',
      avatar: 'SJ'
    },
    {
      name: 'Michael Chen',
      role: 'Desenvolvimento de Negócios na GrowthLabs',
      content: 'A automação é tão natural que os prospects pensam que estou entrando em contato pessoalmente. Resultados incríveis!',
      avatar: 'MC'
    },
    {
      name: 'Emily Rodriguez',
      role: 'Gerente de Marketing na StartupXYZ',
      content: 'Finalmente, uma ferramenta de automação LinkedIn que realmente funciona e mantém minha conta segura.',
      avatar: 'ER'
    }
  ]

  const stats = [
    { label: 'Solicitações de Conexão Enviadas', value: '1.247' },
    { label: 'Taxa de Aceitação', value: '73%' },
    { label: 'Mensagens Enviadas', value: '892' },
    { label: 'Taxa de Resposta', value: '41%' }
  ]

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      {/* Header */}
      <header className="border-b bg-white/80 backdrop-blur-sm sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-sm">SL</span>
              </div>
              <span className="text-xl font-bold text-gray-900">SnapLinked</span>
            </div>
            
            <nav className="hidden md:flex items-center space-x-8">
              <a href="#features" className="text-gray-600 hover:text-blue-600 transition-colors">Recursos</a>
              <a href="#pricing" className="text-gray-600 hover:text-blue-600 transition-colors">Preços</a>
              <a href="#testimonials" className="text-gray-600 hover:text-blue-600 transition-colors">Depoimentos</a>
              <Link to="/login" className="text-gray-600 hover:text-blue-600 transition-colors">Entrar</Link>
            </nav>
            
            <div className="flex items-center space-x-4">
              <Link to="/login">
                <Button variant="ghost" size="sm">Entrar</Button>
              </Link>
              <Link to="/register">
                <Button size="sm">Começar Agora</Button>
              </Link>
            </div>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="py-20 px-4">
        <div className="container mx-auto text-center">
          <div className="inline-flex items-center px-3 py-1 rounded-full text-sm bg-blue-100 text-blue-800 mb-4">
            <Linkedin className="h-4 w-4 mr-2" />
            Automação LinkedIn Simplificada
          </div>
          <h1 className="text-4xl md:text-6xl font-bold text-gray-900 mb-6">
            Automatize Seu <span className="text-blue-600">Networking</span> no LinkedIn
          </h1>
          <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
            Escale seu networking no LinkedIn com automação inteligente. Envie solicitações de conexão personalizadas, 
            mensagens de follow-up e expanda sua rede profissional enquanto você dorme.
          </p>
          
          <div className="flex flex-col sm:flex-row gap-4 justify-center mb-8">
            <Link to="/register">
              <Button size="lg" className="text-lg px-8 py-3">
                Teste Grátis por 14 Dias
                <ArrowRight className="ml-2 h-5 w-5" />
              </Button>
            </Link>
            <Button variant="outline" size="lg" className="text-lg px-8 py-3">
              <Play className="mr-2 h-5 w-5" />
              Assistir Demo
            </Button>
          </div>
          
          <div className="flex flex-wrap justify-center gap-6 text-sm text-gray-600">
            <div className="flex items-center">
              <CheckCircle className="h-4 w-4 text-green-500 mr-2" />
              Teste grátis de 14 dias
            </div>
            <div className="flex items-center">
              <CheckCircle className="h-4 w-4 text-green-500 mr-2" />
              Sem cartão de crédito necessário
            </div>
            <div className="flex items-center">
              <CheckCircle className="h-4 w-4 text-green-500 mr-2" />
              Cancele a qualquer momento
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-20 px-4 bg-white">
        <div className="container mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Tudo Que Você Precisa Para Escalar Sua Rede
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Ferramentas poderosas de automação projetadas para ajudá-lo a construir relacionamentos profissionais significativos em escala.
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {features.map((feature, index) => (
              <Card key={index} className="border-0 shadow-lg hover:shadow-xl transition-shadow duration-300">
                <CardHeader>
                  <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mb-4">
                    <feature.icon className="h-6 w-6 text-blue-600" />
                  </div>
                  <CardTitle className="text-xl">{feature.title}</CardTitle>
                </CardHeader>
                <CardContent>
                  <CardDescription className="text-gray-600">
                    {feature.description}
                  </CardDescription>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Benefits Section */}
      <section className="py-20 px-4 bg-gradient-to-r from-blue-600 to-purple-600 text-white">
        <div className="container mx-auto">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            <div>
              <h2 className="text-3xl md:text-4xl font-bold mb-6">
                Transforme Sua Estratégia no LinkedIn
              </h2>
              <p className="text-xl mb-8 text-blue-100">
                Junte-se a milhares de profissionais que revolucionaram sua abordagem de networking com o SnapLinked.
              </p>
              
              <div className="space-y-4">
                {benefits.map((benefit, index) => (
                  <div key={index} className="flex items-start">
                    <CheckCircle className="h-6 w-6 text-green-400 mr-3 mt-0.5 flex-shrink-0" />
                    <span className="text-lg">{benefit}</span>
                  </div>
                ))}
              </div>
            </div>
            
            <div className="grid grid-cols-2 gap-6">
              {stats.map((stat, index) => (
                <Card key={index} className="bg-white/10 backdrop-blur-sm border-white/20">
                  <CardContent className="p-6 text-center">
                    <div className="text-3xl font-bold text-white mb-2">{stat.value}</div>
                    <div className="text-blue-100 text-sm">{stat.label}</div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Testimonials Section */}
      <section id="testimonials" className="py-20 px-4 bg-gray-50">
        <div className="container mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Confiado por Profissionais no Mundo Todo
            </h2>
            <p className="text-xl text-gray-600">
              Veja o que nossos clientes estão dizendo sobre o SnapLinked
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {testimonials.map((testimonial, index) => (
              <Card key={index} className="border-0 shadow-lg">
                <CardContent className="p-6">
                  <div className="flex items-center mb-4">
                    <div className="w-12 h-12 bg-blue-600 rounded-full flex items-center justify-center text-white font-bold mr-4">
                      {testimonial.avatar}
                    </div>
                    <div>
                      <div className="font-semibold text-gray-900">{testimonial.name}</div>
                      <div className="text-sm text-gray-600">{testimonial.role}</div>
                    </div>
                  </div>
                  <p className="text-gray-700 italic">"{testimonial.content}"</p>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-4 bg-white">
        <div className="container mx-auto text-center">
          <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
            Pronto Para Escalar Seu Outreach no LinkedIn?
          </h2>
          <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
            Junte-se a milhares de profissionais que já estão expandindo suas redes com o SnapLinked.
          </p>
          
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link to="/register">
              <Button size="lg" className="text-lg px-8 py-3">
                Começar Teste Grátis
                <ArrowRight className="ml-2 h-5 w-5" />
              </Button>
            </Link>
            <Link to="/pricing">
              <Button variant="outline" size="lg" className="text-lg px-8 py-3">
                Ver Preços
              </Button>
            </Link>
          </div>
          
          <div className="mt-8 text-sm text-gray-500">
            Sem compromisso • Cancele a qualquer momento • Suporte 24/7
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12 px-4">
        <div className="container mx-auto">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div>
              <div className="flex items-center space-x-2 mb-4">
                <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
                  <span className="text-white font-bold text-sm">SL</span>
                </div>
                <span className="text-xl font-bold">SnapLinked</span>
              </div>
              <p className="text-gray-400">
                A plataforma de automação LinkedIn mais confiável para profissionais que querem escalar seu networking.
              </p>
            </div>
            
            <div>
              <h3 className="font-semibold mb-4">Produto</h3>
              <ul className="space-y-2 text-gray-400">
                <li><a href="#features" className="hover:text-white transition-colors">Recursos</a></li>
                <li><a href="#pricing" className="hover:text-white transition-colors">Preços</a></li>
                <li><Link to="/login" className="hover:text-white transition-colors">Entrar</Link></li>
                <li><Link to="/register" className="hover:text-white transition-colors">Registrar</Link></li>
              </ul>
            </div>
            
            <div>
              <h3 className="font-semibold mb-4">Suporte</h3>
              <ul className="space-y-2 text-gray-400">
                <li><a href="#" className="hover:text-white transition-colors">Central de Ajuda</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Documentação</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Contato</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Status</a></li>
              </ul>
            </div>
            
            <div>
              <h3 className="font-semibold mb-4">Legal</h3>
              <ul className="space-y-2 text-gray-400">
                <li><a href="#" className="hover:text-white transition-colors">Privacidade</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Termos</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Cookies</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Licenças</a></li>
              </ul>
            </div>
          </div>
          
          <div className="border-t border-gray-800 mt-8 pt-8 text-center text-gray-400">
            <p>&copy; 2024 SnapLinked. Todos os direitos reservados.</p>
          </div>
        </div>
      </footer>
    </div>
  )
}
