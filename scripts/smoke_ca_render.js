// 渲染冒烟：真跑 renderCA('meet', day1/2/3) —— V4.41.3/V4.42.1 同类事故教训
const fs = require('fs');
const html = fs.readFileSync('/root/.openclaw/workspace/index.html', 'utf8');

// 抽 caData
const c0 = html.indexOf('const caData');
const cc = html.indexOf('const caCalendar');
const caData = eval('(' + html.slice(html.indexOf('{', c0), html.lastIndexOf('};', cc) + 1) + ')');

// 抽渲染函数源码（renderCA 用下一个函数边界截断——其模板里有嵌套模板字面量，brace-walker 会走飞）
function grab(name) {
  const s = html.indexOf('function ' + name + '(');
  if (s < 0) throw new Error('missing ' + name);
  const e = html.indexOf('\nfunction ', s);
  if (e < 0) throw new Error('no end for ' + name);
  return html.slice(s, e);
}

// 单行小函数
function grabLine(name) {
  const s = html.indexOf('function ' + name + '(');
  const e = html.indexOf('\n', s);
  return html.slice(s, e);
}

// 最小真函数
const caLvNormSrc = grabLine('caLvNorm');
const caLvBadgeSrc = grabLine('caLvBadge');
const caLvTagSrc = grabLine('caLvTag');
const caESrc = grabLine('caE');

// 环境
global.location = { hash: '' };
global.document = { querySelectorAll: () => [], getElementById: () => null, createElement: () => ({ style: {}, setAttribute(){}, appendChild(){} }) };
global.caInjectStyles = () => {};
global.caClickWords = (s) => String(s);
global.speak = () => {};
global.caAffixGo = () => {};
global.caWordPopup = () => {};
global.caQuizAnswers = {}; global.caQuizSubmitted = false;
global.caPick = () => {};
global.caSubmit = () => {};

const renderCA = new Function(
  'caData','caInjectStyles','caClickWords','speak','caAffixGo','caWordPopup','caQuizAnswers','caQuizSubmitted','caPick','caSubmit','location',
  caESrc + '\n' + caLvNormSrc + '\n' + caLvBadgeSrc + '\n' + caLvTagSrc + '\n' +
  grab('caCount') + '\n' + grab('renderCA') +
  '\nreturn renderCA;'
)(
  caData, global.caInjectStyles, global.caClickWords, global.speak, global.caAffixGo, global.caWordPopup,
  global.caQuizAnswers, global.caQuizSubmitted, global.caPick, global.caSubmit, global.location
);

let fail = 0;
for (const day of [1, 2, 3]) {
  try {
    const el = { innerHTML: '' };
    renderCA(el, 'meet', day, true);
    const h = el.innerHTML;
    const checks = [
      ['CA 进阶', h.includes('CA 进阶')],
      ['词汇块', h.includes('① 词汇')],
      ['句型块', h.includes('③ 万能句型')],
      ['词缀块', h.includes('⑤ 词缀专项')],
      ['测验块', h.includes('⑥ 每日一测')],
      ['非空', h.length > 8000],
      ['无undefined', !h.includes('undefined')],
      ['审计表基础标签', h.includes('基础1 / 进阶4 / 专业2')],
    ];
    const bad = checks.filter(c => !c[1]);
    if (bad.length) { fail++; console.log('Day' + day + ' FAIL:', bad.map(b => b[0]).join(',')); }
    else console.log('Day' + day + ' render PASS · len=' + h.length);
  } catch (e) {
    fail++;
    console.log('Day' + day + ' THROW:', e.message);
  }
}
// 其他话题回归
for (const t of ['interview', 'biz_listen', 'biz_speak', 'negotiation']) {
  try {
    const el = { innerHTML: '' };
    renderCA(el, t, 1, true);
    el.innerHTML.length > 5000 ? console.log(t + ' day1 PASS') : (fail++, console.log(t + ' day1 TOO SHORT'));
  } catch (e) { fail++; console.log(t + ' THROW:', e.message); }
}
console.log(fail ? ('FAIL=' + fail) : 'ALL RENDER PASS');
process.exit(fail ? 1 : 0);
