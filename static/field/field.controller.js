
(function () {
  'use strict';

  angular
    .module('horizon.dashboard.sysadmin.workorder.field')
    .controller('WorkOrderFieldModalController', WorkOrderFieldModalController)


  WorkOrderFieldModalController.$inject = [
     '$scope',
     'horizon.dashboard.sysadmin.workorder.field.FieldService',
     'horizon.framework.widgets.toast.service',
     '$location',
     '$window',
     '$rootScope',
   ];

    

  function WorkOrderFieldModalController($scope,FieldService,toastService,$location,$window,$rootScope) {
    var ctrl = this;
    var fieldtype = angular.element("#fieldtype").val();
    var field = angular.element("#field").val();
    var fieldname = angular.element("#fieldname").val();
    var fieldvalue = angular.element("#fieldvalue").val();
    var fielddesc = angular.element("#fielddesc").val();
    var field_choices = angular.element('.field_choices');
    var field_checkbox = angular.element('.field_req');

    var count = 0;

    ctrl.reqfield = 1;
    $scope.workorder_field = fieldname;
    $scope.workorder_desc = fielddesc;
    if (fieldvalue != 'None'){
      $scope.workorder_value = fieldvalue;
    }

    ctrl.submit = function(){
      if ($scope.workorder_desc && $scope.workorder_field){
        var data = FieldService.addField(fieldtype,$scope.workorder_field,$scope.workorder_desc,$scope.workorder_value,ctrl.reqfield);
        data.then(function(obj){
          var url = '/sysadmin/workorder/field';
          window.location.href = url;
        });
      }else if(!$scope.workorder_field){
        toastService.add('error', gettext('字段名不能为空!'));
      }else if(!$scope.workorder_desc){
        toastService.add('error', gettext('字段描述不能为空!'));
      }else{
        toastService.add('error', gettext('未知错误,请联系管理员!'));        
      }
    }

    ctrl.update = function(){
      if ($scope.workorder_desc && $scope.workorder_field){
        // console.log(field_checkbox);
        // for (){
        //   if (field_checkbox.checked){
        //     console.log(field_checkbox).value;
        //   }          
        // }
        var data = FieldService.updateField(field,fieldtype,$scope.workorder_field,$scope.workorder_desc,$scope.workorder_value,ctrl.reqfield);
        data.then(function(obj){
          var url = '/sysadmin/workorder/field';
          window.location.href = url;
        });
      }else if(!$scope.workorder_field){
        toastService.add('error', gettext('字段名不能为空!'));
      }else if(!$scope.workorder_desc){
        toastService.add('error', gettext('字段描述不能为空!'));
      }else{
        toastService.add('error', gettext('未知错误,请联系管理员!'));        
      }
    }

    // ctrl.updateChoice = function(){
    //   for (var i=0;i<field_choices.length;i++){
    //     console.log(field_choices[i]['id']+field_choices[i]['value']);
    //   }
    // }

    $scope.choices = [];

    ctrl.init = function(){
      if (field_choices.length >0){
        for (var i=0;i<field_choices.length;i++){
          $scope.choices.push({'id':field_choices[i]['name'],'name':field_choices[i]['value']});
        }        
      }

      // if(field_checkbox.length >0){
      //   for (var i=0;i<field_checkbox.length;i++){
      //     $scope.
      //   }
      // }


    }

    ctrl.init();

    ctrl.addChoice = function(){
      var newItemNo = $scope.choices.length+1;
      $scope.choices.push({'id':'choice'+newItemNo});
    }

    ctrl.removeChoice = function(e){
      var lastItem = e.choice.id;
      for (var i=0;i<$scope.choices.length;i++){
        if ($scope.choices[i].id === lastItem){
          $scope.choices.splice(i,1);
        }
      }
    }

    ctrl.choiceSubmit = function(){
      var workorder_value = [];
      for (var i=0;i<$scope.choices.length;i++){
        workorder_value.push({'id':$scope.choices[i].id,'name':angular.element("#"+$scope.choices[i].id).val()});
      };
      if ($scope.workorder_desc && $scope.workorder_field){      
        var data = FieldService.addField(fieldtype,$scope.workorder_field,$scope.workorder_desc,workorder_value);
        data.then(function(obj){
          var url = '/sysadmin/workorder/field';
          window.location.href = url;
        });
      }else if(!$scope.workorder_field){
        toastService.add('error', gettext('字段名不能为空!'));
      }else if(!$scope.workorder_desc){
        toastService.add('error', gettext('字段描述不能为空!'));
      }else{
        toastService.add('error', gettext('未知错误,请联系管理员!'));        
      }
    } 


    ctrl.choiceUpdate = function(){
      var workorder_value = [];
      for (var i=0;i<$scope.choices.length;i++){
        workorder_value.push({'id':$scope.choices[i].id,'name':angular.element("#"+$scope.choices[i].id).val()});
      };
      if ($scope.workorder_desc && $scope.workorder_field){      
        var data = FieldService.updateField(field,fieldtype,$scope.workorder_field,$scope.workorder_desc,workorder_value);
        data.then(function(){
          var url = '/sysadmin/workorder/field';
          window.location.href = url;
        });
      }else if(!$scope.workorder_field){
        toastService.add('error', gettext('字段名不能为空!'));
      }else if(!$scope.workorder_desc){
        toastService.add('error', gettext('字段描述不能为空!'));
      }else{
        toastService.add('error', gettext('未知错误,请联系管理员!'));        
      }

    }

  }



})();
