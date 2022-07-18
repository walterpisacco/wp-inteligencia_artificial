$(document).ready(function() {

});	

$('#webcamInput').on('change',function(){
	if($('#webcamInput option:selected').val() < 4){
		$('#ruta').css('display','none');
	}else{
		$('#ruta').css('display','');
		$('#ruta').val('');
	}
})

$('#view').on('switch-change', function () {
    if($('#view').bootstrapSwitch('status') == true){
			Reproducir();
    }else{
    	Detener();
    }
});

function Reproducir(){
		var camera = 0;
		if($('#webcamInput').val() < 4 ) {
			camera = $('#webcamInput').val();
		}
		if($('#webcamInput').val() == 4 ) {
			camera = $('#ruta').val();
		}
		
		var webcamId= $('#webcamInput option:selected').val();

		$.ajax({
			data : {
				serie : '0',
				webcam : camera,
				webcamId : webcamId,
				tipo : 'entrenar',
				label : 'Presencia.txt',
				modelo : 'Presencia.tflite',
				opcion : '0',
				iot: '0'
			},
			type : 'POST',
			url : '/process'
		})
		.done(function(data) {
			if (data.error) {
				$('#errorAlert').text(data.error).show();
				$('#successAlert').hide();
			} else {
				d = new Date();
				$('#video_validado').find('img').attr("src", "/video_feed?"+d.getTime());
				$('#errorAlert').hide();
			}
		});
		event.preventDefault();
}

function Detener(){
		$.ajax({data : {},type : 'GET',url : '/video_feed_detener'});
		event.preventDefault();
}

function getBase64Image(img) {
  var canvas = document.createElement("canvas");
  canvas.width = img.width;
  canvas.height = img.height;
  var ctx = canvas.getContext("2d");
  ctx.drawImage(img, 0, 0);
  var dataURL = canvas.toDataURL();
  return dataURL;
}

$('#btnFotograma').on('click',function(){
	var name = $('#nombreArchivo').val();
	if (name == ''){
		bootbox.alert({ message:'INGRESE UN NOMBRE PARA IDENTIFICAR A LA PERSONA!!',backdrop: true});
		return;
	}
	var imgbase64 = getBase64Image(document.getElementById("video"));
		toggleGifLoad();
		return $.ajax({url:'/Imagen_Guardar',
			data:{name:name,imgbase64:imgbase64},
			type:'POST',dataType:'json',async:true})
		 .always(toggleGifLoad)
		 .done(function(result){
			 if (result == 'true'){
		 		bootbox.alert({ message:'OK',backdrop: true});
			 }else{
			 	bootbox.alert({ message:'ERROR AL INTENTAR GRABAR, INTENTE NUEVAMENTE!!',backdrop: true});
			 }
		 }); 
})

$('#btnEntrenar').on('click',function(){
		 Entrenar();
});

function Entrenar(){
	  $('#view').bootstrapSwitch('setState', false);
		toggleGifLoadReco();
		return $.ajax({url:'/Imagen_Entrenar',
			data:{},
			type:'POST',dataType:'json',async:true})
		 .always(toggleGifLoadReco)
		 .done(function(result){
			 if (result.success == 'true'){
			 	bootbox.alert({ message:'Entrenado de imágenes realizado con éxito!!',backdrop: true});
			 }else{
			 	bootbox.alert({ message:'ERROR AL INTENTAR GRABAR, INTENTE NUEVAMENTE!!',backdrop: true});
			 }
		 }); 
}

$("#uploadedFile").change(function(){
	$('#ruta').val($('#uploadedFile')[0].files[0].name);
});

$('#btnEjecutar').on('click',function(){
	bootbox.confirm({
	    message: "Esta seguro que desea comenzar el análisis?",
	    buttons: {
	        confirm: {
	            label: 'Aceptar',
	            className: 'btn-success'
	        },
	        cancel: {
	            label: 'Cancelar',
	            className: 'btn-default'
	        }
	    },
	    callback: function (result) {
		    if(result == true){
		    	//Grabar();
				Reproducir();		    	
		    }
	    }
	});
});

function Limpiar(){
		toggleGifLoad();
		return $.ajax({url:'/Imagen_Limpiar',
			data:{},
			type:'POST',dataType:'json',async:true})
		 .always(toggleGifLoad)
		 .done(function(result){
			 if (result.success == 'true'){
			 	bootbox.alert({ message:'Registro de imágenes limpiado con éxito!!',backdrop: true});
			 }else{
			 	bootbox.alert({ message:'ERROR AL INTENTAR LIMPIAR EL REGISTRO DE IMÁGENES, INTENTE NUEVAMENTE!!',backdrop: true});
			 }
		 }); 
}

$('#btnLimpiar').on('click',function(){
		 Limpiar();
});

function limpiar(){
	$('.limp').val('');
	$('.limp').text('');
}


