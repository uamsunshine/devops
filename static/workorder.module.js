

(function () {
  'use strict';


  angular
    .module('horizon.dashboard.sysadmin.workorder', [
    'horizon.dashboard.sysadmin.workorder.field',
    'horizon.dashboard.sysadmin.workorder.order',
    'horizon.dashboard.sysadmin.workorder.message',
    'horizon.dashboard.sysadmin.workorder.list',
    'horizon.dashboard.sysadmin.workorder.eff',
    ])
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
    var path = $windowProvider.$get().STATIC_URL + 'dashboard/sysadmin/workorder/';
    $provide.constant('horizon.dashboard.sysadmin.workorder.basePath', path);
  }

})();
