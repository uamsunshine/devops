
(function () {
  'use strict';

  angular
    .module('horizon.dashboard.sysadmin.workorder.order')
    .controller('ListModalController', ListModalController)


  ListModalController.$inject = [
     '$scope',
     'horizon.dashboard.sysadmin.workorder.list.ListService',
     'horizon.framework.widgets.toast.service',
     '$location',
     '$window',
     '$rootScope',
     '$http',
   ];

    

  function ListModalController($scope,ListService,$location,$window,$rootScope,$http) {
    var ctrl = this;

    ctrl.submit = function (id) {
      console.log(id);
    }


  }



})();
