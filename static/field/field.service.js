;(function () {
  'use strict';

  angular
    .module('horizon.dashboard.sysadmin.workorder.field')
    .factory('horizon.dashboard.sysadmin.workorder.field.FieldService', FieldService)

  FieldService.$inject = [
    '$q',
    'horizon.framework.util.http.service',
    'horizon.framework.widgets.toast.service',
   ];

  function FieldService($q, apiService, toastService,$scope) {

    var model = {
      addField : addField,
      updateField : updateField,
    };

    function addField(fieldtype,workorder_field,workorder_desc,workorder_value,reqfield){
      var data = JSON.stringify({'fieldtype':fieldtype,'workorder_field':workorder_field,'workorder_desc':workorder_desc,'workorder_value':workorder_value,'reqfield':reqfield});
      return apiService.post('/sysadmin/workorder/field/create',data)
          .error(function(obj){
            console.log(obj);
            toastService.add('error', gettext('字段名重复'));
          });
    }

    function updateField(field,fieldtype,workorder_field,workorder_desc,workorder_value,reqfield){
      var data = JSON.stringify({'field':field,'fieldtype':fieldtype,'workorder_field':workorder_field,'workorder_desc':workorder_desc,'workorder_value':workorder_value,'reqfield':reqfield});
      var config = {headers: { 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'},}
      return apiService.post('/sysadmin/workorder/field/update',data,config)
          .error(function(obj){
            toastService.add('error', gettext('字段名重复'));
          });      
    }


    return model;
  }

})();
