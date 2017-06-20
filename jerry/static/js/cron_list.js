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
        //var host = document.getElementById("host")
        var host = document.getElementById("host")
        var host = host.options[host.selectedIndex]
        var script = document.getElementById("script")
        var script = script.options[script.selectedIndex]
        var cron = F.cron
        var sc_path = F.sc_path
        var cmd = F.cmd
        var comment = F.comment
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
                            alert("添加成功！");
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



