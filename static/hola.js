console.log('hola')
// try {
//   document.querySelector('footer.main-footer ').innerHTML =
//     '<strong>Copyright © 2022. By GoDjango</strong> Todos los derechos reservados.'
// } catch (e) {
//   console.log(e)
// }
try {
  document.querySelector('div.login-logo').innerHTML =
    '<h2><img src="/static/img/icon.png" style="width: 80px;height: auto;" alt="EnCAJA Lite">EnCAJA Lite</h2>'
} catch (e) {
  console.log(e)
}
// try {
//   document.querySelector('#jazzy-logo img').src = '/static/img/icon.png'
//   document.querySelector('#jazzy-logo img').style = 'opacity:1'
// } catch (e) {
//   console.log(e)
// }
if (window.location.pathname.includes('sale')) {
  try {
    document.querySelector('h4.card-title').innerText = 'Listado de ventas'
  } catch (e) {
    console.log(e)
  }
}