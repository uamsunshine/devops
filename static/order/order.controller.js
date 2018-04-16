
(function () {
  'use strict';

  angular
	.module('horizon.dashboard.sysadmin.workorder.order')
	.controller('WorkOrderModalController', WorkOrderModalController)


  WorkOrderModalController.$inject = [
	 '$scope',
	 'horizon.dashboard.sysadmin.workorder.order.OrderService',
	 'horizon.framework.widgets.toast.service',
	 '$location',
	 '$window',
	 '$rootScope',
	 'FileUploader',
   ];

	

  function WorkOrderModalController($scope,OrderService,toastService,$location,$window,$rootScope,FileUploader) {
	var ctrl = this;
	var field_select_num = angular.element('.field_select_num');
	var field_text_num = angular.element('.field_text_num');
	var field_textarea_num = angular.element('.field_textarea_num');
	var field_radio_num = angular.element('.field_radio_num');
	var field_checkbox_num = angular.element('.field_checkbox_num');
	var field_multiple_num = angular.element('.field_multiple_num');
	var priority = angular.element('.priority');
	var field_type_select = angular.element('#select_field').val();
	var field_type_text = angular.element('#text_field').val();
	var field_type_textarea = angular.element('#textarea_field').val();
	var field_type_radio = angular.element('#radio_field').val();
	var field_type_checkbox = angular.element('#checkbox_field').val();
	var field_type_multiple = angular.element('#multiple_field').val();

	var temp_id = angular.element('#temp_id').val();
	var userid = angular.element('#userid').val();
	var default_send = angular.element('#default_send').val();
	var index_cc = document.getElementById('order_cc');

	var order_cc = [];
	var field_obj = {};
	var field_priority = {};
	var files = [];
	var reader = new FileReader();
	var data_file = new FormData();
	$scope.is_submit = false;


	ctrl.getFile = function(e){
	  $scope.$apply(function () {
		  for (var i = 0; i < e.files.length; i++) {
			  if (e.files[i]){                
				files.push(e.files[i]);
			  }else{
				toastService.add('error',gettext('请添加文件'));
			  }

		  }
		  ctrl.queue = files;
	  });
	}

	ctrl.remove = function(e){
	  for (var i=0;i<ctrl.queue.length;i++){
		if (ctrl.queue[i].name == e.item.name){
		  ctrl.queue.splice(i,1);
		}
	  }
	}

	ctrl.submit = function () {
	  var is_error = 'False';
	  $scope.is_submit = true;
	  for (var i in ctrl.queue){
		data_file.append('files',files[i]);
	  }

	  if (field_type_select){
		for (var i=0;i<field_select_num.length;i++){
		  var selected_index = document.getElementById("field_"+field_select_num[i].value);
		  field_obj[angular.element("#label_"+field_select_num[i].value).text()] = selected_index.options[selected_index.selectedIndex].text;
		  if (!selected_index.options[selected_index.selectedIndex].text){
            $scope.is_submit = false;
			is_error = 'True';
			toastService.add('error', gettext(angular.element("#label_"+field_select_num[i].value).text()+'--不能为空!'));
		  }
		}
	  }

	  if (index_cc){
		for (var i=0;i<index_cc.length;i++){
		  if (index_cc.options[i].selected){
			order_cc.push(index_cc.options[i].value);
		  }
		}
	  }

	  if (field_type_multiple){
		for (var i=0;i<field_multiple_num.length;i++){
		  var multiple_index = document.getElementById("field_"+field_multiple_num[i].value);
		  var multiple_value = '';
		  for (var n=0;n<multiple_index.length;n++){
			if (multiple_index.options[n].selected){
			  multiple_value = multiple_value + multiple_index.options[n].text + ' - ';
			}
		  }
		  field_obj[angular.element("#label_"+field_multiple_num[i].value).text()] = multiple_value;
		  if (!multiple_value){
            $scope.is_submit = false;
			is_error = 'True';
			toastService.add('error', gettext(angular.element("#label_"+field_multiple_num[i].value).text()+'--不能为空!'));
		  }
		}
	  }

	  if (field_type_text){
		for (var i=0;i<field_text_num.length;i++){
		  field_obj[angular.element("#label_"+field_text_num[i].value).text()] = angular.element("#field_"+field_text_num[i].value).val();
		  if (!angular.element("#field_"+field_text_num[i].value).val()){
            $scope.is_submit = false;
			is_error = 'True';
			toastService.add('error', gettext(angular.element("#label_"+field_text_num[i].value).text()+'--不能为空!'));
		  }
		}
	  }

	  if (field_type_textarea){
		for (var i=0;i<field_textarea_num.length;i++){
		  field_obj[angular.element("#label_"+field_textarea_num[i].value).text()] = angular.element("#field_"+field_textarea_num[i].value).val();
		  if (!angular.element("#field_"+field_textarea_num[i].value).val()){
            $scope.is_submit = false;
			is_error = 'True';
			toastService.add('error', gettext(angular.element("#label_"+field_textarea_num[i].value).text()+'---不能为空!'));            
		  }
		}
	  }

	  if (field_type_radio){
		for(var i=0;i<field_radio_num.length;i++){
		  var radio_field = angular.element('.field_'+field_radio_num[i].value);
		  for(var n=0;n<radio_field.length;n++){
			if(radio_field[n].checked){
			  field_obj[angular.element("#label_"+field_radio_num[i].value).text()] = radio_field[n].value;
			}
		  }
		  if (!field_obj[angular.element("#label_"+field_radio_num[i].value).text()]){
			$scope.is_submit = false;
			is_error = 'True';
			toastService.add('error', gettext(angular.element("#label_"+field_radio_num[i].value).text()+'---不能为空!'));            
		  }
		}
	  }

	  if (field_type_checkbox){
		for(var i=0;i<field_checkbox_num.length;i++){
		  var checkbox_field = angular.element('.field_'+field_checkbox_num[i].value);
		  var checked_value = '';
		  for(var n=0;n<checkbox_field.length;n++){
			if(checkbox_field[n].checked){
			  checked_value = checked_value + checkbox_field[n].value + ' | ';
			}
		  }
		  field_obj[angular.element("#label_"+field_checkbox_num[i].value).text()] = checked_value;
		  if (!checked_value){
			$scope.is_submit = false;
			is_error = 'True';
			toastService.add('error', gettext(angular.element("#label_"+field_checkbox_num[i].value).text()+'---不能为空!'));            
		  }
		}
	  }

	  data_file.append('field_obj',JSON.stringify(field_obj));
	  data_file.append('userid',userid);
	  data_file.append('order_name',$scope.order_name);
	  data_file.append('order_desc',$scope.order_desc);
	  data_file.append('temp_id',temp_id);
	  data_file.append('order_cc',JSON.stringify(order_cc));

	  if (is_error == 'False'){
		var data = OrderService.addOrder(data_file);
		data.then(function(obj){
		  if (obj['data']['result'] == false){
			toastService.add('success', gettext(obj['data']['msg']));
			$scope.is_submit = false;
		  }
		  if (obj['data']['result'] == true){
			if (obj['data']['id']){
			  var url = '/sysadmin/workorder/'+obj['data']['id']+'/list/';
			  window.location.href = url;
			}
		  }
		});
	  }

	}

  }



})();
