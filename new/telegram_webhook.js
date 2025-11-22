// Cloudflare Worker для відправки замовлень в Telegram
// Деплой: https://workers.cloudflare.com/

export default {
  async fetch(request, env) {
    // CORS headers
    const corsHeaders = {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
    };

    // Handle CORS preflight
    if (request.method === 'OPTIONS') {
      return new Response(null, { headers: corsHeaders });
    }

    if (request.method !== 'POST') {
      return new Response('Method not allowed', { 
        status: 405,
        headers: corsHeaders 
      });
    }

    try {
      const data = await request.json();
      
      // Telegram Bot Token (додайте в Worker Environment Variables)
      const BOT_TOKEN = env.TELEGRAM_BOT_TOKEN || '8242972523:AAHrhraZ2dir1Arn32nLSnPPT1RZe9XSVuQ';
      const CHAT_ID = env.TELEGRAM_CHAT_ID; // ID чату Арсена (треба отримати)
      
      // Форматування повідомлення
      const serviceEmojis = {
        'concert': '🎭',
        'evenement-prive': '💍',
        'enseignement': '🎓',
        'enregistrement': '🎙️'
      };

      const serviceNames = {
        'concert': 'Concert',
        'evenement-prive': 'Événement privé',
        'enseignement': 'Enseignement musical',
        'enregistrement': 'Enregistrement'
      };

      const emoji = serviceEmojis[data.serviceType] || '🎵';
      const serviceName = serviceNames[data.serviceType] || data.serviceType;

      const message = `
${emoji} <b>NOUVELLE DEMANDE: ${serviceName}</b>

👤 <b>Contact:</b>
   ${data.contactName}
   ${data.contactEmail}
   ${data.phone || 'Non fourni'}

📅 <b>Date:</b> ${data.eventDate || 'À discuter'}
📍 <b>Lieu:</b> ${data.eventLocation || 'À discuter'}

💬 <b>Détails:</b>
${data.repertoireDetails || 'Aucun détail supplémentaire'}

🌐 <b>Langue:</b> ${data.language === 'uk' ? '🇺🇦 Українська' : '🇫🇷 Français'}
⏰ <b>Reçu:</b> ${new Date().toLocaleString('fr-FR', { timeZone: 'Europe/Zurich' })}
      `.trim();

      // Відправка в Telegram
      const telegramUrl = `https://api.telegram.org/bot${BOT_TOKEN}/sendMessage`;
      
      const telegramResponse = await fetch(telegramUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          chat_id: CHAT_ID,
          text: message,
          parse_mode: 'HTML'
        })
      });

      const telegramData = await telegramResponse.json();

      if (!telegramData.ok) {
        console.error('Telegram error:', telegramData);
        throw new Error(telegramData.description || 'Telegram API error');
      }

      return new Response(JSON.stringify({ 
        success: true, 
        message: 'Demande envoyée avec succès!' 
      }), {
        status: 200,
        headers: {
          'Content-Type': 'application/json',
          ...corsHeaders
        }
      });

    } catch (error) {
      console.error('Error:', error);
      return new Response(JSON.stringify({ 
        success: false, 
        error: error.message 
      }), {
        status: 500,
        headers: {
          'Content-Type': 'application/json',
          ...corsHeaders
        }
      });
    }
  }
};