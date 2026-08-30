const https = require('https');
const fs = require('fs');
const path = require('path');

const HISTORY_DIR = path.join(__dirname, '..', 'mir-data', 'history');
const SYMBOLS = {
  'NI0': { name: '沪镍主力', unit: '元/吨', source: 'Sina Futures' },
  'AL0': { name: '沪铝主力', unit: '元/吨', source: 'Sina Futures' },
  'ZC0': { name: '动力煤主力', unit: '元/吨', source: 'Sina Futures' },
  'AO0': { name: '氧化铝主力', unit: '元/吨', source: 'Sina Futures' },
  'I0':  { name: '铁矿石主力', unit: '元/吨', source: 'Sina Futures' },
};

function fetchSinaKLine(symbol) {
  return new Promise((resolve, reject) => {
    const url = `https://stock.finance.sina.com.cn/futures/api/jsonp.php/var=/InnerFuturesNewService.getDailyKLine?symbol=${symbol}`;
    https.get(url, { timeout: 15000 }, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const match = data.match(/var=\((.*)\)/s);
          if (!match) { reject(new Error('Invalid JSONP')); return; }
          resolve(JSON.parse(match[1]));
        } catch (e) { reject(e); }
      });
    }).on('error', reject);
  });
}

function dailyToWeekly(dailyData) {
  if (!dailyData || dailyData.length === 0) return [];
  const sorted = [...dailyData].sort((a, b) => a.d.localeCompare(b.d));
  const weeks = [];
  let currentWeek = null;
  for (const day of sorted) {
    const date = new Date(day.d);
    const weekStart = new Date(date);
    weekStart.setDate(date.getDate() - date.getDay() + 1);
    const weekKey = weekStart.toISOString().slice(0, 10);
    if (!currentWeek || currentWeek.week !== weekKey) {
      if (currentWeek) weeks.push(currentWeek);
      currentWeek = { week: weekKey, open: parseFloat(day.o), high: parseFloat(day.h), low: parseFloat(day.l), close: parseFloat(day.c), volume: parseInt(day.v) || 0 };
    } else {
      currentWeek.high = Math.max(currentWeek.high, parseFloat(day.h));
      currentWeek.low = Math.min(currentWeek.low, parseFloat(day.l));
      currentWeek.close = parseFloat(day.c);
      currentWeek.volume += parseInt(day.v) || 0;
    }
  }
  if (currentWeek) weeks.push(currentWeek);
  return weeks.slice(-52);
}

async function updateHistory(symbol) {
  const config = SYMBOLS[symbol];
  console.log(`Fetching ${symbol} (${config.name})...`);
  try {
    const dailyData = await fetchSinaKLine(symbol);
    const weeklyData = dailyToWeekly(dailyData);
    const output = { symbol, name: config.name, unit: config.unit, source: config.source, interval: '1wk', lastUpdated: new Date().toISOString(), data: weeklyData };
    fs.writeFileSync(path.join(HISTORY_DIR, `${symbol}.json`), JSON.stringify(output, null, 2));
    console.log(`  Saved ${weeklyData.length} weeks`);
    return output;
  } catch (e) {
    console.error(`  ERROR: ${e.message}`);
    return null;
  }
}

async function main() {
  if (!fs.existsSync(HISTORY_DIR)) fs.mkdirSync(HISTORY_DIR, { recursive: true });
  for (const symbol of Object.keys(SYMBOLS)) await updateHistory(symbol);
  console.log('Done');
}
main().catch(console.error);
