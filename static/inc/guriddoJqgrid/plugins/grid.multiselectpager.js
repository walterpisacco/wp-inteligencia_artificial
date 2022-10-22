;(function($){
	/**
	 * jqGrid extension
	 * Pablo Ruhl pabloalejandroruhl@gmail.com
	 *
	 * @version: 1.0 - 22/06/2016
	 * 
	 * Dual licensed under the MIT and GPL licenses:
	 * http://www.opensource.org/licenses/mit-license.php
	 * http://www.gnu.org/licenses/gpl-2.0.html
	**/	
	$.jgrid.extend({
		/**
		* Add row selected to memory array
		* 
		* @return Array
		**/
		_addSelectedRows:function(a,b,c,d,e){
			var $t = $(this);
			var saveSelectedRows = $t.getGridParam('selarrrow')
		    page                 = $t.getGridParam('page'),
		    allRowSelecteds      = $t.data('allRowSelecteds') || [];
		    allRowSelecteds[page.toString()] = saveSelectedRows
		    $t.data('allRowSelecteds',allRowSelecteds);
		    return Array.prototype.concat.apply([], allRowSelecteds).filter(function(n){return n != undefined});
		},
		/**
		 * Select all rows in the paging according what has been previously selected
		 *
		 * @return Array
		 **/
		_populateSelectedRows:function(){
			var $t                   = $(this)
			    currentPage          = $t.getGridParam('page').toString(),
	            retrieveSelectedRows = $t.data('allRowSelecteds') || [];
			$.each(Array.prototype.concat.apply([], retrieveSelectedRows), function (index, value) {
				$t.setSelection(value, false);
			});
			return Array.prototype.concat.apply([], retrieveSelectedRows).filter(function(n){return n != undefined});
		},
		/**
		 * Force selected only with checkbox		 * 
		 * @see http://www.trirand.com/jqgridwiki/doku.php?id=wiki:events
		 * 
		 * @return Boolean
		 */
		_onlySelectedCheckbox:function(rowid,parent,e){
			return $(e.target).is(':checkbox');
		},
		/**
		 * Retrieve all selected records acrros of the pages
		 * 
		 * @return Array
		 **/
		getAllSelectedRows:function(){
			var $t = $(this);
			retrieveSelectedRows = $t.data('allRowSelecteds') || [];
			return Array.prototype.concat.apply([], retrieveSelectedRows).filter(function(n){return n != undefined});
		},
		/**
		 * Constructor
		 */
		multiSelectPager:function(){
			var $t = $(this);
			if(!$t[0].grid){ return;}
			// check Multiselect
			if($(this).getGridParam('multiselect')){
				$(this).on('jqGridSelectRow jqGridSelectAll',$t._addSelectedRows);
				$(this).on('jqGridGridComplete',$t._populateSelectedRows);
				$(this).on('jqGridBeforeSelectRow',$t._onlySelectedCheckbox);
			}
		}
	})
})(jQuery)