(function () {
  'use strict';

  angular
    .module('horizon.dashboard.sysadmin.workorder.order')
    .factory('horizon.dashboard.sysadmin.workorder.order.OrderService', OrderService)

  OrderService.$inject = [
    '$q',
    'horizon.framework.util.http.service',
    'horizon.framework.widgets.toast.service',
    '$window',
   ];

  function OrderService($q, apiService, toastService,$scope,$window) {

    var model = {
      addOrder : addOrder,
      sendOrder:sendOrder,
    };

    function sendOrder(){
      // body = {}
      // body['user'] = send_user_id
      // body['msg'] = '主题:{0}\n描述:{1}\n来自:{2}\n时间:{3}\n'.format(temp_obj.name,temp_obj.description,UserManager.get(id=userid).username,time_now)
      // url = 'http://omg.mogoroom.com/api/dingding/message/send?accessToken=YWP3g0Mb2HMhOCLpRauk'    
      // headers = { 'Content-Type': 'application/json' }
      // req = urllib2.Request(url, json.dumps(body, ensure_ascii=True), headers)
      // response = urllib2.urlopen(req).read()
    }


    function addOrder(data_file){
      var config = {'headers': {'Content-Type':undefined},'transformRequest': angular.identity}
      return apiService.post('/sysadmin/workorder/order/create',data_file,config)
          // .success(function(obj){
          //   toastService.add('success', gettext(obj['msg']));
          //   // window.location.reload();
          // })
          .error(function(obj){
            console.log(obj);
            toastService.add('error', gettext('提交工单出错'));
          });
    }

    return model;
  }

})();
