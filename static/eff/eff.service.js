;(function () {
  'use strict';

  angular
    .module('horizon.dashboard.sysadmin.workorder.field')
    .factory('horizon.dashboard.sysadmin.workorder.field.EffService', EffService)

  EffService.$inject = [
    '$q',
    'horizon.framework.util.http.service',
    'horizon.framework.widgets.toast.service',
   ];

  function EffService($q, apiService, toastService,$scope) {

    var model = {
      init : init,
    };

    function init(begintime,endtime){
      var config = {'params': {'begintime':begintime,'endtime':endtime}};
      return apiService.get('/sysadmin/workorder/efficiency/list',config)
          .error(function(obj){
            toastService.add('error', gettext('获取数据失败'));
          });
    }



    return model;
  }

})();
