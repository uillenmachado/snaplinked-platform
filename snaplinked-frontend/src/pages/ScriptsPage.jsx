import React, { useState } from 'react';

const ScriptsPage = () => {
  const [selectedScript, setSelectedScript] = useState('connection');


  const scripts = {
    connection: {
      name: 'Solicitações de Conexão',
      description: 'Script para enviar solicitações de conexão automaticamente',
      code: `// 🚀 SCRIPT DE CONEXÕES AUTOMÁTICAS
// Cole este código no console do LinkedIn (F12)

conectarPorPalavraChave("desenvolvedor", 25, "Olá! Gostaria de me conectar com você.");

// Parâmetros:
// 1. "desenvolvedor" - palavra-chave para busca
// 2. 25 - máximo de conexões
// 3. "mensagem" - mensagem personalizada (opcional)`
    },
    viewing: {
      name: 'Visualização de Perfis',
      description: 'Script para visualizar perfis automaticamente',
      code: `// 👀 SCRIPT DE VISUALIZAÇÃO DE PERFIS
// Cole este código no console do LinkedIn (F12)

visualizarPerfis("CEO startup", 50);

// Parâmetros:
// 1. "CEO startup" - palavra-chave para busca
// 2. 50 - máximo de perfis para visualizar`
    },
    messaging: {
      name: 'Mensagens Automáticas',
      description: 'Script para enviar mensagens para conexões existentes',
      code: `// 💬 SCRIPT DE MENSAGENS AUTOMÁTICAS
// Cole este código no console do LinkedIn (F12)

// Primeiro, navegue para suas conexões
// Depois execute:

const mensagem = \`Olá! 

Espero que esteja bem. Gostaria de conversar sobre oportunidades de colaboração.

Abraços!\`;

// Enviar para conexões recentes
SnapLinkedBot.autoMessage(mensagem, 10);`
    },
    complete: {
      name: 'Script Completo',
      description: 'Script completo com todas as funcionalidades',
      code: `// 🔥 SCRIPT COMPLETO SNAPLINKED
// Cole este código no console do LinkedIn (F12)

// Carregar o sistema de automação
fetch('https://19hninc0ejo1.manus.space/scripts/linkedin-automation.js')
  .then(response => response.text())
  .then(script => {
    eval(script);
    console.log('✅ SnapLinked carregado com sucesso!');
  })
  .catch(error => {
    console.error('❌ Erro ao carregar SnapLinked:', error);
  });`
    }
  };

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text).then(() => {
      alert('Script copiado para a área de transferência!');
    });
  };

  const downloadScript = (scriptName, code) => {
    const element = document.createElement('a');
    const file = new Blob([code], { type: 'text/javascript' });
    element.href = URL.createObjectURL(file);
    element.download = `snaplinked-${scriptName}.js`;
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Scripts de Automação</h1>
          <p className="mt-2 text-gray-600">
            Scripts JavaScript para executar no console do LinkedIn e automatizar suas ações
          </p>
        </div>

        {/* Instruções */}
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-6 mb-8">
          <div className="flex">
            <div className="flex-shrink-0">
              <svg className="h-5 w-5 text-blue-400" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
              </svg>
            </div>
            <div className="ml-3">
              <h3 className="text-sm font-medium text-blue-800">
                Como usar os scripts
              </h3>
              <div className="mt-2 text-sm text-blue-700">
                <ol className="list-decimal list-inside space-y-1">
                  <li>Faça login no LinkedIn em uma nova aba</li>
                  <li>Pressione F12 para abrir o console do navegador</li>
                  <li>Cole o script desejado no console</li>
                  <li>Pressione Enter para executar</li>
                  <li>Monitore a execução através dos logs no console</li>
                </ol>
              </div>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Lista de Scripts */}
          <div className="lg:col-span-1">
            <div className="bg-white shadow rounded-lg">
              <div className="px-6 py-4 border-b border-gray-200">
                <h2 className="text-lg font-medium text-gray-900">Scripts Disponíveis</h2>
              </div>
              <div className="p-0">
                {Object.entries(scripts).map(([key, script]) => (
                  <button
                    key={key}
                    onClick={() => setSelectedScript(key)}
                    className={`w-full text-left px-6 py-4 border-b border-gray-100 hover:bg-gray-50 transition-colors ${
                      selectedScript === key ? 'bg-blue-50 border-l-4 border-l-blue-500' : ''
                    }`}
                  >
                    <h3 className="font-medium text-gray-900">{script.name}</h3>
                    <p className="text-sm text-gray-500 mt-1">{script.description}</p>
                  </button>
                ))}
              </div>
            </div>

            {/* Estatísticas */}
            <div className="bg-white shadow rounded-lg mt-6">
              <div className="px-6 py-4 border-b border-gray-200">
                <h2 className="text-lg font-medium text-gray-900">Estatísticas de Uso</h2>
              </div>
              <div className="p-6">
                <div className="space-y-4">
                  <div className="flex justify-between">
                    <span className="text-sm text-gray-600">Scripts executados hoje:</span>
                    <span className="text-sm font-medium text-gray-900">12</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm text-gray-600">Conexões enviadas:</span>
                    <span className="text-sm font-medium text-gray-900">156</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm text-gray-600">Perfis visualizados:</span>
                    <span className="text-sm font-medium text-gray-900">89</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm text-gray-600">Taxa de sucesso:</span>
                    <span className="text-sm font-medium text-green-600">87%</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Visualizador de Script */}
          <div className="lg:col-span-2">
            <div className="bg-white shadow rounded-lg">
              <div className="px-6 py-4 border-b border-gray-200 flex justify-between items-center">
                <h2 className="text-lg font-medium text-gray-900">
                  {scripts[selectedScript].name}
                </h2>
                <div className="flex space-x-2">
                  <button
                    onClick={() => copyToClipboard(scripts[selectedScript].code)}
                    className="inline-flex items-center px-3 py-2 border border-gray-300 shadow-sm text-sm leading-4 font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                  >
                    <svg className="mr-2 h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
                    </svg>
                    Copiar
                  </button>
                  <button
                    onClick={() => downloadScript(selectedScript, scripts[selectedScript].code)}
                    className="inline-flex items-center px-3 py-2 border border-gray-300 shadow-sm text-sm leading-4 font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                  >
                    <svg className="mr-2 h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                    Baixar
                  </button>
                </div>
              </div>
              
              <div className="p-6">
                <p className="text-gray-600 mb-4">{scripts[selectedScript].description}</p>
                
                {/* Editor de código */}
                <div className="bg-gray-900 rounded-lg p-4 overflow-x-auto">
                  <pre className="text-green-400 text-sm font-mono whitespace-pre-wrap">
                    {scripts[selectedScript].code}
                  </pre>
                </div>

                {/* Instruções específicas */}
                <div className="mt-6 bg-yellow-50 border border-yellow-200 rounded-lg p-4">
                  <div className="flex">
                    <div className="flex-shrink-0">
                      <svg className="h-5 w-5 text-yellow-400" viewBox="0 0 20 20" fill="currentColor">
                        <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                      </svg>
                    </div>
                    <div className="ml-3">
                      <h3 className="text-sm font-medium text-yellow-800">
                        Importante
                      </h3>
                      <div className="mt-2 text-sm text-yellow-700">
                        <ul className="list-disc list-inside space-y-1">
                          <li>Execute apenas no LinkedIn oficial (linkedin.com)</li>
                          <li>Respeite os limites diários para evitar bloqueios</li>
                          <li>Monitore sempre a execução através do console</li>
                          <li>Use mensagens personalizadas e relevantes</li>
                          <li>Pare a automação se detectar comportamento anômalo</li>
                        </ul>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Comandos de Controle */}
            <div className="bg-white shadow rounded-lg mt-6">
              <div className="px-6 py-4 border-b border-gray-200">
                <h2 className="text-lg font-medium text-gray-900">Comandos de Controle</h2>
              </div>
              <div className="p-6">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="bg-gray-50 rounded-lg p-4">
                    <h3 className="font-medium text-gray-900 mb-2">Parar Automação</h3>
                    <code className="text-sm bg-gray-900 text-green-400 p-2 rounded block">
                      pararAutomacao()
                    </code>
                  </div>
                  
                  <div className="bg-gray-50 rounded-lg p-4">
                    <h3 className="font-medium text-gray-900 mb-2">Ver Estatísticas</h3>
                    <code className="text-sm bg-gray-900 text-green-400 p-2 rounded block">
                      estatisticas()
                    </code>
                  </div>
                  
                  <div className="bg-gray-50 rounded-lg p-4">
                    <h3 className="font-medium text-gray-900 mb-2">Resetar Contadores</h3>
                    <code className="text-sm bg-gray-900 text-green-400 p-2 rounded block">
                      SnapLinkedBot.resetStats()
                    </code>
                  </div>
                  
                  <div className="bg-gray-50 rounded-lg p-4">
                    <h3 className="font-medium text-gray-900 mb-2">Configurar Limites</h3>
                    <code className="text-sm bg-gray-900 text-green-400 p-2 rounded block">
                      SnapLinkedBot.config.dailyConnectionLimit = 30
                    </code>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ScriptsPage;
