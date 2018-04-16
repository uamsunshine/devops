

(function () {
  'use strict';


  angular
    .module('horizon.dashboard.sysadmin.workorder.list', [])
    .config(config);

  config.$inject = [
    '$provide',
    '$windowProvider'
  ];

  /**
   * @name horizon.dashboard.project.basePath
   * @description Base path for the project dashboard
   */
  function config($provide, $windowProvider) {
    var path = $windowProvider.$get().STATIC_URL + 'dashboard/sysadmin/workorder/list/';
    $provide.constant('horizon.dashboard.sysadmin.workorder.list.basePath', path);
  }

})();
