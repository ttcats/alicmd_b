// 是否禁用
function isDisable()
{
    return confirm('确定禁用该条配置？');
}

// 是否启用
function isEnable()
{
    return confirm('确定启用该条配置？');
}

// 是否删除
function isDel()
{
    return confirm('确定删除该条配置？');
    //var a=confirm('确定删除该条配置？');
    //if (a == true)
    //{document.write("恭喜你答对了！")}
}

// 新增
function AddOps() {
	//document.getElementById("AddTr").style.display = "none"; 
    document.getElementById("AddTr").style.display = "table-row";
}

// 取消新增
function CancellNullOps() {
	document.getElementById("AddTr").style.display = "none"; 
    //document.getElementById("AddTr").style.display = "inline";
}

// 重置表单
function ResetForm(FormID) {
	document.getElementById(FormID).reset();
	document.getElementById('AddType').focus();
	
}

// 提交新增
function SubmitOps() {
	document.AddForm.submit();
}

// 编辑模式与取消编辑模式
function EditOps(ShowID,HideID) {
	document.getElementById(HideID).style.display = "none"; 
    document.getElementById(ShowID).style.display = "table-row";
}

// 保存编辑后的结果
function SaveOps(FormID) {
    document.getElementById(FormID).submit();
}

// 删除表单
function Delasset(id,hostname) {
    var a=confirm('确定删除主机'+hostname+'信息?');
    if (a == true)
    { $.get('/cmdb/asset/del/',
      {id:id},
      function(data){
        if (data=='true'){
        window.location.reload();
      } else {
        alert('error');
      }}
   );}
}


// ansible更新
function Updateasset(id) {
    $.get('/cmdb/asset/update/',
      {id:id},
      function(data){
      if (data=='true'){
      window.location.reload();
      } else {
        alert(data)
      }
  });
}




function GetQueryString(name)
{
     var reg = new RegExp("(^|&)"+ name +"=([^&]*)(&|$)");
     var r = window.location.search.substr(1).match(reg);
     if(r!=null)return  unescape(r[2]); return null;
}



function ChangeParam(name,value)
 {
  var url=window.location.href ;
  var newUrl="";
var reg = new RegExp("(^|)"+ name +"=([^&]*)(|$)");
var tmp = name + "=" + value;
if(url.match(reg) != null)
{
 newUrl= url.replace(eval(reg),tmp);
}
else
{
 if(url.match("[\?]"))
 {
 newUrl= url + "&" + tmp;
 }
 else
 {
 newUrl= url + "?" + tmp;
 }
}
   location.href=newUrl;
 }


function Keyword(data) {
    window.location.href='/cmdb/asset/'+'?search='+data
    //var psel = document.getElementById("keyword");
    //psel.value = data;
    //var url=document.URL;
    //var searchURL = window.location.search;
    //search = GetQueryString("search");
    //newurl = ChangeParam('search',data)
    //page = GetQueryString("page");
    //window.location.href=url+"&search="+data
    //$.get(url,{'search':data});
}



function Delops(FormID) {
    var a=confirm('确定删除该条配置？');
    if (a == true)
    {var xmlhttp;
    xmlhttp=new XMLHttpRequest();
    xmlhttp.onreadystatechange=function()
    {
    if (xmlhttp.readyState==4 && xmlhttp.status==200)
        {
        document.getElementById("myDiv").innerHTML=xmlhttp.responseText;
        }
    }
    xmlhttp.open("GET",FormID,true);
    xmlhttp.send();
    window.location.reload();
    }
}


function onSearches(selectID,row){
	$.ajax({
	type:"get",
	url:"/options",
        async:true,
        data:{selid:$("#show4type").val()},
        sucess:function(msg){
	alert("true");},
});
}



function getService(){
	var module=document.getElementById("module");
	var module = module.options[module.selectedIndex];
	var ansiblescript = document.getElementById("ansiblescript");
	if ( module.value == "copy" ){
		ansiblescript.placeholder = 'like this: src=/root/a.sh dest=/tmp/';
	} else if ( module.value == "file" ){
		ansiblescript.placeholder = 'like this: dest=/tmp/t.sh mode=755 owner=root group=root';
	} else if ( module.value == "cron" ){
		ansiblescript.placeholder = 'like this: name="custom job" minute=*/3 hour=* day=* month=* weekday=* job="/usr/sbin/ntpdate 172.16.254.139"';
	} else if ( module.value == "group" ){
		ansiblescript.placeholder = 'like this: gid=2014 name=nolinux';
	} else if ( module.value == "user" ){
		ansiblescript.placeholder = 'like this: name=nolinux groups=nolinux state=present';
	} else if ( module.value == "yum" ){
		ansiblescript.placeholder = 'like this: state=present name=httpd';
	} else if ( module.value == "service" ){
		ansiblescript.placeholder = 'like this: name=puppet state=restarted enabled=yes';
	} else if ( module.value == "script" ){
		ansiblescript.placeholder = 'like this: /root/a.sh';
	} else if ( module.value == "ping" ){
		ansiblescript.placeholder = '无需填写';
	} else if ( module.value == "command" ){
		ansiblescript.placeholder = 'like this: hostname';
	} else if ( module.value == "raw" ){
		ansiblescript.placeholder = 'like this: hostname|tee';
	} else if ( module.value == "get_url" ){
		ansiblescript.placeholder = 'like this: url=http://10.1.1.116/favicon.ico dest=/tmp';
	} else if ( module.value == "synchronize" ){
		ansiblescript.placeholder = 'like this: src=/root/a dest=/tmp/ compress=yes';
	} else {
		ansiblescript.placeholder = '';
	}
};
