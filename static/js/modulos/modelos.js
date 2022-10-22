$(document).ready(function() {
	var pageWidth = $("#tblDatos").parent().width() - 100;	
	var formBuscar = $('#searchbox-events'),
	tbDatos = $("#tblDatos").jqGrid({
	    styleUI : 'Bootstrap',
		responsive : true,
		datatype : 'local',
		mtype : 'POST',
	    colNames: ['Codigo','tipo','Modelo','Detalle','Archivo',''],
	    colModel: [{name: 'idModelo',hidden:true,index: '1',width: (pageWidth*(15/100)),align: 'center'},
	               {name: 'Tipo',index: '2',width:(pageWidth*(10/100)),align: 'left',editable:false,editoptions:{size:20,disabled:'disabled'},search:true,formoptions:{elmsuffix:"(*)",rowpos:4}},
	               {name: 'Modelo',index: '3',width:(pageWidth*(30/100)),align: 'left',editable:false,editoptions:{size:20,disabled:'disabled'},search:true,formoptions:{elmsuffix:"(*)",rowpos:3}},
	               {name: 'Detalle',index: '9',width:(pageWidth*(25/100)),align: 'left',editable:false,editoptions:{size:20,disabled:'disabled'},search:false,formoptions:{elmsuffix:"(*)",rowpos:2}},
	               {name: 'Archivo',index: '9',width:(pageWidth*(30/100)),align: 'left',editable:false,editoptions:{size:20,disabled:'disabled'},search:false,formoptions:{elmsuffix:"(*)",rowpos:2}},
	         	   {name: 'acciones',index: '20',width:(pageWidth*(5/100)),align: 'left',editable:false,editoptions: {readonly: "readonly"}}], 
	               pager: '#pagDatos',
	    rowNum : 30,
	  //  altRows: true,
		autowidth : true,
		refresh: true,		
		height : 'auto',
		rownumbers : false,
		rowList : [ 30, 60, 90 ],
		sortname : 2,
		sortorder : 'ASC',
		viewrecords : true,
		gridview : true,
		caption : '',
		shrinkToFit : true,
		cellEdit: false,
       	cmTemplate : {
			'sortable' : false,
			'resize' : false,
			'editable' : true,
			'search' : false
		},
		rowattr:function(rowData){
		   if(rowData.estado == "Eliminado") return {"style":"color: lightcoral;"};
	    },
		loadComplete : function(data) {
		    $("tr.jqgrow:odd").addClass('myAltRowClassEven');
		    $("tr.jqgrow:even").addClass('myAltRowClassOdd');
		},
		loadError : function(xhr, st, err) {
			jQuery("#rsperror").html("Type: " + st + "; Response: "+ xhr.status + " " + xhr.statusText);
		}, /**/
		gridComplete : function(){
			$('#wrapper').on('toggle-out toggle-in',
					function(e) {
						tbDatos.trigger('resize');
					});
		}
	}).navGrid('#pagDatos', {edit : false,add : false,del : false,view : false,search : false,refresh : true});

if(isMobile.any()) {
	$("#tblDatos").hideCol("Tipo");	
	$("#tblDatos").hideCol("Detalle");
	$("#tblDatos").hideCol("Archivo");
	$("#tblDatos").setGridWidth($(window).width()-70); 
}

	function Buscar() {
		  var fields = formBuscar.find(':input').serializeArray();
	      var postdata = tbDatos.jqGrid('getGridParam', 'postData');
			    postdata.filters = formatFilter(fields);//La funcion esta en fngenerales
		        tbDatos.jqGrid('setGridParam', {
		        datatype: 'json',
		        url: "/ModelosList_get",
				async:true,
	          stringResult: true,search: true,postData: postdata,page:1
	      }).trigger('reloadGrid');
	}

	Buscar();

});

function AgregaModelo(){
	$('#spArchivo').text('Ningún Archivo Seleccionado');
	limpiar();
	$('#modalImportar').modal('show');
}

$("#uploadedFile").change(function(){
	$('#spArchivo').text(this.value);
});

function GuardarImportacion(){
    if (validateFields($('#formModelos :input').not('button')) || $('#spArchivo').text() == 'Ningún Archivo Seleccionado'){
    	bootbox.alert('Seleccione un archivo y complete los campos marcados como obligatorios');
    	return;
    }	
	var formData = {};
	var tipo = $('#tipo').val()
    var file = $('#uploadedFile')[0].files[0];
    var modelo = $('#modelo').val().replace(" ", "_");
    var descripcion = $('#descripcion').val()

	var formData = new FormData();
	formData.append('tipo',tipo);
    formData.append('file',file);
	formData.append('modelo',modelo);
	formData.append('descripcion',descripcion);

	toggleGifLoad();
	$.ajax({url:'Modelo_Guardar',
		data:formData,
		type:'POST',
		contentType: false,
		processData: false,
		async:true})
		 .always(toggleGifLoad)	
		 .done(function(result){
		 	$('#modalImportar').modal('hide');	
		 	$('#tblDatos').trigger("reloadGrid");
		 bootbox.alert({ message:result.Text,backdrop: true});
	 	});
}

function EliminarModelo(){
	selRowId = $("#tblDatos").jqGrid ('getGridParam', 'selrow');
    celidModelo = $("#tblDatos").jqGrid ('getCell', selRowId, 'idModelo');	
	bootbox.confirm({
	    message: "Esta seguro que desea eliminar?",
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
		    	Eliminar(celidModelo);
		    }
	    }
	});
}


function Eliminar(id){
	toggleGifLoad();
		return $.ajax({url:'Modelo_Eliminar',
			data : {idModelo : id},
			type:'POST',dataType:'json',async:true})
		 .always(toggleGifLoad)
		 .done(function(result){
			 	$('#tblDatos').trigger("reloadGrid");
			 	bootbox.alert({ message:result.Text,backdrop: true});
		 });
}


