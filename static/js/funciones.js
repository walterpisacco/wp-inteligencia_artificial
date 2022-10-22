
$(function ()
{ $(".tip").popover();
});

if(localStorage.getItem("lang") =='en'){
  var locale = 'en';
  messageDel = "Are you sure you want to delete?";
  messageSave = "Are you sure you want to save?";
  messageClear = "Are you sure you want to clear?";
}else{
  var locale = 'es';
  messageDel = "Esta seguro que desea eliminar?";
  messageSave = "Esta seguro que desea guardar?";
  messageClear = "Esta seguro que desea limpiar";
}

function cerrar(){
  bootbox.confirm({
    message: "Esta seguro que deseas cerrar?",
    buttons: {
        confirm: {
            label: 'Aceptar',
            className: 'btn-danger'
        },
        cancel: {
            label: 'Cancelar',
            className: 'btn-default'
        }
    },
    callback: function (result) {
      if(result == true){
        window.close();
      }
    }
  });
}

function abrirPerfil(){
  $('#modalPerfil').modal('show');
}

$('#btnCancelar').on('click',function(){
  $('#modalPerfil').modal('hide');
});

function limpiar(){
  $('.limp').val('');
  $('.limp').text('');
}

function formatFilter(params) {
  var filterGroup = {'groupOp': 'AND',op: 'eq',text: 'any','rules': []},
    filterObject= {'field': '','op': 'eq','data': ''};
  filterGroup.rules = _.filter(params, function(elem) {
    return (!_.isEmpty(elem.value) && !_.isUndefined(elem.value) && elem.value !== '-1');
  }).map(function(elem) {
     
    var rule = _.clone(filterObject);
    rule.field = elem.name;
    rule.data = elem.value;
     
    return rule;
  });
  return JSON.stringify(filterGroup);
}

function hexToRGB(a, e) {
  var i = parseInt(a.slice(1, 3), 16),
      n = parseInt(a.slice(3, 5), 16),
      s = parseInt(a.slice(5, 7), 16);
  return e ? "rgba(" + i + ", " + n + ", " + s + ", " + e + ")" : "rgb(" + i + ", " + n + ", " + s + ")"
}

md.initFormExtendedDatetimepickers();

function toggleGifLoad(){
  $('#preloader').toggle();
}

function toggleGifLoadReco(){
  $('#preloaderReco').toggle();
}

function validateFields(fields){
  var error1 = false;
    _.map(fields,function(field){
      if($(field).hasClass('fieldRequired')){
        error = _isEmpty($.trim($(field).val()));
        if(error){
          error1 = true;  
          setElementError($(field));
        }
      }
      
      if($(field).hasClass('isNumeric')){
        error = _isNumeric($(field).val());
        if(error){
          error1 = true;  
          setElementError($(field));
        }
      }
    });
    return error1;
}

/**
 * Setea con un error un elemento
 * @param {jQuery.Object} elem
 * @return void
 */
function setElementError(elem){
  elem.addClass('mod_error').bind('focus change mouseenter',function(){
    removeElementError($(this));
  });
}

/**
 * Remueve el error del elemento
 * @param {jQuery.Object} elem
 * @return void
 */
function removeElementError(elem){
  elem.removeClass('mod_error');
}

/**
 * Valida que no este vacio, no sea indefinido y que no sea NaN
 * 
 * @param {String||Numeric||Integer} value
 * @return Boolean
 */
function _isEmpty(value){
  var value = String(value);
  return (_.isEmpty(value) || _.isUndefined(value) || _.isNaN(value)) ? true : false;
}

/**
 * Valida que sea numerico
 * 
 * @param Numeric||Integer value
 * @return Boolean
 */
function _isNumeric(value){
  return (/^([0-9])*$/.test(value))? true:false;
}

/**
 * Valida que no contenga caracteres especiales
 * 
 * @param String
 * @retunr Boolean
 */
function _isSpecialChar(value){
  return (String(value).length > 0 && /^[a-zA-Z0-9 Ã¡Ã©Ã­Ã³ÃºAÃ‰Ã�Ã'ÃšÃ‘Ã± '\u00e1\u00e9\u00ed\u00f3\u00fa\u00c1\u00c9\u00cd\u00d3\u00da\u00f1\u00d1\u00FC\u00DC \-.\,]+$/.test(value))? false:true;
}

/**
 * Valida que sea un DNI
 * 
 * @param String
 * @return Boolean
 */
function _isDocumento(value){
  return (/^([0-9]){8}$/.test(value))? true:false;
}

function fechaNacional(fecha){
  dia = fecha.substring(fecha.length - 2, fecha.length);
  mes = fecha.substring(7, 5);
  anio = fecha.substring(0, 4);
  fecha = dia + '/' + mes + '/' + anio;
  return fecha;  
}

function fechaInternacional(fecha){
  anio = fecha.substring(fecha.length - 4, fecha.length);
  mes = fecha.substring(5, 3);
  dia = fecha.substring(0, 2);
  fecha = anio + '-' + mes + '-' + dia;
  return fecha;
}

var isMobile = {
    Android: function() {return navigator.userAgent.match(/Android/i);},
    BlackBerry: function() {return navigator.userAgent.match(/BlackBerry/i);},
    iOS: function() {return navigator.userAgent.match(/iPhone|iPad|iPod/i);},
    Opera: function() {return navigator.userAgent.match(/Opera Mini/i);},
    Windows: function() {return navigator.userAgent.match(/IEMobile/i);},
    any: function() {return (isMobile.Android() || isMobile.BlackBerry() || isMobile.iOS() || isMobile.Opera() || isMobile.Windows());}
};

/*************** set estilo ***********/
if(localStorage.getItem("css") =='fix.css'){
  $('#chkCss').bootstrapSwitch('setState', false);
}else{
  $('#chkCss').bootstrapSwitch('setState', true);
}

$('#chkCss').on('switch-change', function () {
    if($('#chkCss').bootstrapSwitch('status') == true){
         localStorage.setItem("css","fix_dark.css");
         CambiarConfig('estilo','fix_dark.css');
    }else{
        localStorage.setItem("css","fix.css");
        CambiarConfig('estilo','fix.css');
    }
});

/*********************** set lenguaje ******************/
if(localStorage.getItem("lang") =='sp'){
  $('#chkLang').bootstrapSwitch('setState', true);
}else{
  $('#chkLang').bootstrapSwitch('setState', false);
}

$('#chkLang').on('switch-change', function () {
    if($('#chkLang').bootstrapSwitch('status') == true){
         localStorage.setItem("lang","sp");
         CambiarConfig('lenguaje','sp');
    }else{
        localStorage.setItem("lang","en");
        CambiarConfig('lenguaje','en');
    }
});

function CambiarConfig(tipo, valor){
  $.ajax({url:'../Utilidades/Search/CambiarConfig.php',data:{tipo:tipo,valor:valor},type:'POST',dataType:'json',async:true})
  .done(function(result){
   location.reload();
   });
}