
function isDel()
{
    return confirm('确定删除该条配置？');
}


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


function dbcreate(formId) {
        var xmlHttp = createXmlHttp();
        if(!xmlHttp) {
                alert("您的浏览器不支持AJAX！");
                return 0;
        }
        var F = document.getElementById(formId);

        var hostname = F.hostname;
        var port = F.port;
        var group_id = F.group_id.value;
        var m_hostname = F.m_hostname.value;
        var m_port = F.m_port.value;
        if(hostname.value=='')
           {
               alert('请输入主机名！');
               hostname.focus();
               return false;
           }
        if(port.value=='')
           {
               alert('请输入端口！');
               port.focus();
               return false;
           }
        var e = document.getElementById(formId);
        var url = e.action;
        var postData = "hostname="+hostname.value+"&port="+port.value+"&group_id="+group_id+"&m_hostname="+m_hostname+"&m_port="+m_port;
        xmlHttp.open("POST", url, true);
        xmlHttp.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
        xmlHttp.send(postData);
        xmlHttp.onreadystatechange = function() {
                if(xmlHttp.readyState == 4 && xmlHttp.status == 200) {
                        var PostAnswer=xmlHttp.responseText;
                        if(PostAnswer=="sucess")
                            {
                            alert("添加成功！");
                            window.location.href="/opera/db_info";
                            }
                        else if (PostAnswer=="err")
                           {
                            alert("系统故障！");
                            return false;
                            }
                        else {
                            alert("服务器也木有知道哪儿出错了(┬＿┬)");
                            return false;
                            }
                    }
                }
}

