function createXmlHttp() {
	var xmlHttp = null;
	try {
		xmlHttp = new XMLHttpRequest();
	} catch (e) {
		try {
			xmlHttp = new ActiveXObject("Msxml2.XMLHTTP");
		} catch (e) {
			xmlHttp = new ActiveXObject("Microsoft.XMLHTTP");
		}
	}
	return xmlHttp;
}

function submitForm(formId) {
	var xmlHttp = createXmlHttp();
	if(!xmlHttp) {
		alert("您的浏览器不支持AJAX！");
		return 0;
	}
        var F = document.getElementById(formId);
        var id = F.id
        var idc = document.getElementById("idc")
        var idc = idc.options[idc.selectedIndex]
        var groups = document.getElementById("groups")
        var grouplist = ''
	for (i=0; i<groups.length; i++) {
		if (groups.options[i].selected == true) {
			grouplist += groups.options[i].value + " ";
		}
	}
        var hostname = F.hostname
        var host_ip = F.host_ip
        var ssh_port = F.ssh_port
        var radio = document.getElementsByName("stat")
        for (i=0; i<radio.length; i++) {
		if (radio[i].checked) { 
			stat = radio[i].value;
		}
	}
        if(hostname.value=='')
           {
               alert('请输入主机名！');
               hostname.focus();
               return false;
           }
        if(host_ip.value=='')
           {
               alert('请输入主机ip！');
               host_ip.focus();
               return false;
           }
        if(idc.value=='')
           {
               alert('请选择idc机房！');
               return false;
           }
        if(grouplist=='')
           {
               alert('请选择所属主机组！');
               //sc_path.focus();
               return false;
           }
	var e = document.getElementById(formId);
	var url = e.action;
	var postData = "hostname="+hostname.value+"&host_ip="+host_ip.value+"&ssh_port="+ssh_port.value+"&idc="+idc.value+"&groups="+grouplist+"&status="+stat;
	xmlHttp.open("POST", url, true);
	xmlHttp.setRequestHeader("Content-Type", "application/x-www-form-urlencoded"); 
	xmlHttp.send(postData);
	xmlHttp.onreadystatechange = function() {
		if(xmlHttp.readyState == 4 && xmlHttp.status == 200) {
			var PostAnswer=xmlHttp.responseText;
                        if(PostAnswer=="Add.True") 
                            {
                            alert("添加成功！");
                            window.location.href="/cmdb/asset";
                            }
                        else {
                            alert(PostAnswer);
                            return false;
                            }
		    }
	        }
}


function submiteditForm(formId) {
	var xmlHttp = createXmlHttp();
	if(!xmlHttp) {
		alert("您的浏览器不支持AJAX！");
		return 0;
	}
        var thisurl = document.URL
        var F = document.getElementById(formId);
        var id = F.id
        var idc = document.getElementById("idc")
        var idc = idc.options[idc.selectedIndex]
        var groups = document.getElementById("groups")
        var grouplist = ''
	for (i=0; i<groups.length; i++) {
		if (groups.options[i].selected == true) {
			grouplist += groups.options[i].value + " ";
		}
	}
        var hostname = F.hostname
        var host_ip = F.host_ip
        var ssh_port = F.ssh_port.value
        var remote_ip = F.remote_ip.value
        var brand = F.brand.value
        var cpu = F.cpu.value
        var mac = F.mac.value
        var memory = F.memory.value
        var disk = F.disk.value
        var system_type = F.system_type.value
        var system_version = F.system_version.value
        var system_arch = F.system_arch.value
        var number = F.number.value
        var sn = F.sn.value
        var cabinet = F.cabinet.value
        var comment = F.comment.value
        var asset_type = document.getElementById("asset_type")
        var asset_type = asset_type.options[asset_type.selectedIndex]
        var asset_env = document.getElementById("asset_env")
        var asset_env = asset_env.options[asset_env.selectedIndex]
        var asset_status = document.getElementById("asset_status")
        var asset_status = asset_status.options[asset_status.selectedIndex]
        var radio = document.getElementsByName("is_active")
        for (i=0; i<radio.length; i++) {
		if (radio[i].checked) { 
			is_active = radio[i].value;
		}
	}
        if(hostname.value=='')
           {
               alert('请输入主机名！');
               hostname.focus();
               return false;
           }
        if(host_ip.value=='')
           {
               alert('请输入主机ip！');
               host_ip.focus();
               return false;
           }
        if(idc.value=='')
           {
               alert('请选择idc机房！');
               return false;
           }
        if(grouplist=='')
           {
               alert('请选择所属主机组！');
               //sc_path.focus();
               return false;
           }
	var e = document.getElementById(formId);
	var url = e.action;
	var postData = "hostname="+hostname.value+"&host_ip="+host_ip.value+"&ssh_port="+ssh_port+"&idc="+idc.value+"&groups="+grouplist+"&mac="+mac+"&is_active="+is_active+"&remote_ip="+remote_ip+"&brand="+brand+"&cpu="+cpu+"&memory="+memory+"&disk="+disk+"&system_type="+system_type+"&system_version="+system_version+"&system_arch="+system_arch+"&number="+number+"&sn="+sn+"&cabinet="+cabinet+"&comment="+comment+"&asset_type="+asset_type.value+"&asset_env="+asset_env.value+"&asset_status="+asset_status.value;
	xmlHttp.open("POST", url, true);
	xmlHttp.setRequestHeader("Content-Type", "application/x-www-form-urlencoded"); 
	xmlHttp.send(postData);
	xmlHttp.onreadystatechange = function() {
		if(xmlHttp.readyState == 4 && xmlHttp.status == 200) {
			var PostAnswer=xmlHttp.responseText;
                        if(PostAnswer=="Add.True") 
                            {
                            alert("编辑成功！");
                            window.location.href="/cmdb/asset";
                            }
                        else {
                            alert(PostAnswer);
                            return false;
                            }
		    }
	        }
}



function submitFormSave(formId) {
	var xmlHttp = createXmlHttp();
	if(!xmlHttp) {
		alert("您的浏览器不支持AJAX！");
		return 0;
	}
        var F = document.getElementById(formId);
        var id = F.id_save
        //var host = document.getElementById("host")
        var HostID = "host_save" + id.value;
        var ScriptID = "script_save" + id.value;
        //var host = document.getElementById("host_save")
        var host = document.getElementById(HostID)
        var host = host.options[host.selectedIndex]
        //var script = document.getElementById("script_save")
        var script = document.getElementById(ScriptID)
        var script = script.options[script.selectedIndex]
        var cron = F.cron_save
        var cmd = F.cmd_save
        var sc_path = F.sc_path_save
        var comment = F.comment_save
        if(host.value=='')
           {
               alert('请选择主机！');
               return false;
           }
        if(cron.value=='')
           {
               alert('请输入cron表达式！');
               return false;
           }
        if(script.value=='')
           {
               alert('请选择本机脚本！');
               script.focus();
               return false;
           }
        if(sc_path.value=='')
           {
               alert('请输入目标主机脚本存放路径！');
               sc_path.focus();
               return false;
           }
	var e = document.getElementById(formId);
	var url = e.action;
	var postData = "host="+host.value+"&cron="+cron.value+"&script="+script.value+"&cmd="+cmd.value+"&comment="+comment.value+"&sc_path="+sc_path.value;
	xmlHttp.open("POST", url, true);
	xmlHttp.setRequestHeader("Content-Type", "application/x-www-form-urlencoded"); 
	xmlHttp.send(postData);
	xmlHttp.onreadystatechange = function() {
		if(xmlHttp.readyState == 4 && xmlHttp.status == 200) {
			var PostAnswer=xmlHttp.responseText;
                        if(PostAnswer=="Add.True") 
                            {
                            alert("修改成功！");
                            window.location.href="/cron/list";
                            }
                        else if (PostAnswer=="Error")
                           {
                            alert("填写错误或Salt故障！");
                            return false;
                            }
                        else if (PostAnswer=="Cron.Error")
                           {
                            alert("创建定时任务失败！");
                            return false;
                            }
                        else if (PostAnswer=="Cp.Error")
                           {
                            alert("同步脚本文件失败！");
                            return false;
                            }
                        else {
                            alert("服务器也木有知道哪儿出错了(┬＿┬)");
                            return false;
                            }
		    }
	        }
}



