// 返回发送请求的包
function request(link,data,type="POST") {
    const pack={
        url:link,
        data:data,
        type:type,
        cache:false,
        contentType:false,
        processData:false,
        success:(response)=>reload(response),
        error:(jqXHR,textStatus,errorThrown)=>console.log(`${textStatus}:${errorThrown}`),
    };
    console.log(pack);
    return pack
};

// 返回并更新页面
function reload(response) {
    console.log(response);
    if (response.code) {
        if (response.type=="upload") {
            pushFile(response.files);
        } else if (response.type=="delete") {
            pullFile(response.file)
        } else {
            setTimeout(()=>$("body").fadeToggle("slow"),550);
            setTimeout(()=>location.reload(),550);
        }
    }
    openWarned(response.code?"Success":"Failure",response.text);
};

// 打开提示框
function openWarned(type,text) {
    $("#warningH").text(type);
    $("#warning").text(text);
    $(".warnedBox").show();
}

// 关闭提示框
function closeWarned() {
    $(".warnedBox").fadeToggle("fast");
}

// 页面加载后立马执行=>阻止表单默认提交行为
$(document).ready(()=>{
    $("form").submit(function(event) {
        event.preventDefault();
        const formData=new FormData(this);
        if (this.id=="upload") {
            const fileList=$("#file")[0].files;
            for (let i=0;i<fileList.length;i++) {
                formData.append("files[]",fileList[i]);
            };
        };
        $.ajax(request(this.id,formData));
    });
});