(function () {
  'use strict';

  angular
    .module('horizon.dashboard.sysadmin.workorder.list')
    .factory('horizon.dashboard.sysadmin.workorder.list.ListService', ListService)

  ListService.$inject = [
    '$q',
    'horizon.framework.util.http.service',
    'horizon.framework.widgets.toast.service',
    '$http',
   ];

  function ListService($q, apiService, toastService,$http) {

    var model = {
      getOrderTemp:getOrderTemp,
    };


    function getOrderTemp(id){
      var config = {'params': {'id': id}};
      return apiService.get('/sysadmin/workorder/temp/type/list/', config)
          .error(function (obj) {
            console.log(obj);
            toastService.add('error', gettext('操作失败'));
          });
    }

    return model;
  }

})();
