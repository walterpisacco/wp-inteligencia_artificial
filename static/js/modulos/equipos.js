$(document).ready(function() {
	var pageWidth = $("#tblDatos").parent().width() - 100;	
	var formBuscar = $('#searchbox-events'),
	tbDatos = $("#tblDatos").jqGrid({
	    styleUI : 'Bootstrap',
		responsive : true,
		datatype : 'local',
		mtype : 'POST',
	    colNames: ['Codigo','Nombre','Serie','Tipo','Marca y Modelo','Estado','','','',''],
	    colModel: [{name: 'celidEquipo',hidden:true,index: '1',width: (pageWidth*(0/100)),align: 'center'},
	               {name: 'Nombre',index: '2',width:(pageWidth*(20/100)),align: 'left',editable:false,editoptions:{size:20,disabled:'disabled'},search:true,formoptions:{elmsuffix:"(*)",rowpos:4}},
	               {name: 'Serie',index: '3',width:(pageWidth*(15/100)),align: 'left',editable:false,editoptions:{size:20,disabled:'disabled'},search:true,formoptions:{elmsuffix:"(*)",rowpos:3}},
	               {name: 'Tipo',index: '4',width:(pageWidth*(15/100)),align: 'left',editable:false,editoptions:{size:20,disabled:'disabled'},search:true,formoptions:{elmsuffix:"(*)",rowpos:2}},
	               {name: 'Marca',index: '5',width:(pageWidth*(30/100)),align: 'left',editable:false,editoptions:{size:20,disabled:'disabled'},search:false,formoptions:{elmsuffix:"(*)",rowpos:2}},
	               {name: 'Estado',index: '6',width:(pageWidth*(10/100)),align: 'center',editable:false,editoptions:{size:20,disabled:'disabled'},search:false,formoptions:{elmsuffix:"(*)",rowpos:2}},
				   {name: 'Direccion',hidden:true,index: '7',width: (pageWidth*(0/100)),align: 'center'},
				   {name: 'Lat',hidden:true,index: '7',width: (pageWidth*(0/100)),align: 'center'},
				   {name: 'Lon',hidden:true,index: '7',width: (pageWidth*(0/100)),align: 'center'},
	         	   {name: 'acciones',index: '20',width:(pageWidth*(10/100)),align: 'left',editable:false,editoptions: {readonly: "readonly"}}], 
	               pager: '#pagDatos',
	    rowNum : 10,
	  //  altRows: true,
		autowidth : true,
		refresh: true,		
		height : 'auto',
		rownumbers : false,
		rowList : [ 10, 20, 30 ],
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
	$("#tblDatos").hideCol("Serie");
	$("#tblDatos").hideCol("Tipo");
	$("#tblDatos").hideCol("Marca");
	$("#tblDatos").hideCol("Estado");
	$("#tblDatos").setGridWidth($(window).width()-70); 
}

	function Buscar() {
		  var fields = formBuscar.find(':input').serializeArray();
	      var postdata = tbDatos.jqGrid('getGridParam', 'postData');
			    postdata.filters = formatFilter(fields);//La funcion esta en fngenerales
		        tbDatos.jqGrid('setGridParam', {
		        datatype: 'json',
		        url: "/EquiposList_get",
				async:true,
	          stringResult: true,search: true,postData: postdata,page:1
	      }).trigger('reloadGrid');
	}

	Buscar();

	$.ajax({url:'/Combos_get',data:{tipo:'TIPOEQUIPO',param:''},type:'POST',dataType:'json',async:true})
	.done(function(result){
	  if(result.length > 0){
	    $.each( result, function( key, value ) {
	      $('#tipo').append('<option value="'+value[0]+'" >'+value[1]+'</option>');
	    });
	     $('#tipo').selectpicker('refresh');
	  }
	});	


});	

function EditarEquipo(){
	limpiar();
	selRowId = $("#tblDatos").jqGrid ('getGridParam', 'selrow');
    celidEquipo = $("#tblDatos").jqGrid ('getCell', selRowId, 'celidEquipo');
    celNombre = $("#tblDatos").jqGrid ('getCell', selRowId, 'Nombre');
    celSerie = $("#tblDatos").jqGrid ('getCell', selRowId, 'Serie');
    celTipo = $("#tblDatos").jqGrid ('getCell', selRowId, 'Tipo');
    celMarca = $("#tblDatos").jqGrid ('getCell', selRowId, 'Marca');
    celEstado = $("#tblDatos").jqGrid ('getCell', selRowId, 'EstadoID');

	$('#idEquipo').val(celidEquipo);
	$('#nombre').val(celNombre);	
	$('#serie').val(celSerie);
	$('#marca').val(celMarca);

	$("#tipo").find('option:contains("'+celTipo+'")').prop('selected', true);
	$('#select2-tipo-container').text( $('#tipo option:selected').text());
	$('#tipo').selectpicker('refresh');

	$("#estado").find('option:contains("'+celEstado+'")').prop('selected', true);
	$('#select2-estado-container').text( $('#estado option:selected').text());
	$('#estado').selectpicker('refresh');	

	$('#modalEquipo').modal('show');	
};

function AgregarEquipo(){
	limpiar();
	$('#modalEquipo').modal('show');
}

$('#btnGuardar').on('click',function(){
	bootbox.confirm({
	    message: '¿Esta seguro que desea guardar?',
	 //   locale: locale,		
	    buttons: {
	        confirm: {
	            className: 'btn-success'
	        },
	        cancel: {
	            className: 'btn-default'
	        }
	    },
	    callback: function (result) {
		    if(result == true){
		    	var dataform = {};
		    	dataform = $('#frmEquipo  :input').serialize().replace(/["']/g, "");
		    	Grabar(dataform);
		    }
	    }
	});
});


function Grabar(dataform){
    if (validateFields($('#frmEquipo :input').not('button'))){
    	bootbox.alert('Los campos marcados, son obligatorios');
    	return;
    }
	toggleGifLoad();
		return $.ajax({url:'/Equipo_Guardar',
			data:dataform,
			type:'POST',dataType:'json',async:true})
		 .always(toggleGifLoad)
		 .done(function(result){
			 if (result[0][1] == 'true'){
		 		bootbox.alert({ message:result[0][0],backdrop: true});
			 	$('#modalEquipo').modal('hide');
		 		$('#tblDatos').trigger("reloadGrid");			 	
			 }
		 }); 
}

function EliminarEquipo(){
	selRowId = $("#tblDatos").jqGrid ('getGridParam', 'selrow');
	celidEquipo = $("#tblDatos").jqGrid ('getCell', selRowId, 'celidEquipo');
	bootbox.confirm({
    message: '¿Esta seguro que desea eliminar?',
 //   locale: locale,		
    buttons: {
        confirm: {
            className: 'btn-success'
        },
        cancel: {
            className: 'btn-default'
        }
    },
    callback: function (result) {
	    if(result == true){
	    	Eliminar(celidEquipo);
	    }
    }
	});
}

function Eliminar(idEquipo){
	toggleGifLoad();
		return $.ajax({url:'/Equipo_Eliminar',
			data:{idEquipo:idEquipo},
			type:'POST',dataType:'json',async:true})
		 .always(toggleGifLoad)
		 .done(function(result){
			 if (result[0][1] == 'true'){
		 		bootbox.alert({ message:result[0][0],backdrop: true});
		 		$('#tblDatos').trigger("reloadGrid");			 	
			 }
		 }); 
}

$( ".modal-dialog" ).draggable();

function limpiar(){
	$('.limp').val('');
	$('.limp').text('');
	$('#idEquipo').val(0);
}


