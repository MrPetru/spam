/* SPAM Spark Project & Asset Manager
 *
 * This file is part of SPAM (Spark Project & Asset Manager).
 *
 * SPAM is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * SPAM is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with SPAM.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Original Copyright (c) 2010, Lorenzo Pierfederici <lpierfederici@gmail.com>
 * Contributor(s): 
 */

var upload = new Object;
upload.uploading = 0;

upload.queue = {length: 0, files: {},
                add_file: function(file) {
                    this.length += 1;
                    this.files[this.length] = file;
                    return this.length;
                },
                find: function(filename) {
                    var found = false;
                    $.each(this.files, function(key, file) {
                        if (file.name == filename)
                            found = true;
                    });
                    return found;
                }
               };

upload.file_read = function(queue_id, file) {
    var reader = new FileReader();
    upload.uploading += 1;
    $(upload.config.submitter).attr('disabled', 'disabled');
    reader.onloadend = function(e) {
        upload.file_upload(queue_id, e.target.result);
    };
    reader.readAsBinaryString(file);
}

upload.handle_files = function(queue, files) {
    for (var i = 0; i < files.length; i++) {
        var file = files[i];

        var splitted_name = file.name.split(".");
        var ext = "." + splitted_name[splitted_name.length-1];
        if (ext != upload.config.ext) {
            alert('"' + file.name + '" is not a "' + upload.config.ext + '" file');
            continue;
        }

        if (!upload.queue.find(file.name)) {
            var n = upload.queue.add_file(file);
            var filediv = $('<div class="queue_item">' +
                            '<div id="upload_progress_' + n + '" class="upload_progress"></div>' +
                            '<div class="obj">' + file.name + '</div>' +
                            '<input type="hidden" name="uploaded" value="' + file.name + '"></input>' +
                            '</div>');
            $(queue).append(filediv);
            var progress = $("#upload_progress_" + n);
            progress.progressbar();
            upload.file_read(n, file);
        }
    }
}

upload.file_upload = function(queue_id, fileData) {
    var progress = $("#upload_progress_" + queue_id);
    var file = upload.queue.files[queue_id];
    var xhr = new XMLHttpRequest();

    $(xhr.upload).bind("progress", function(e) {
        var oe = e.originalEvent;
        //console.log('progress event', oe);
        if (oe.lengthComputable) {
            var percentage = Math.round((oe.loaded * 100) / oe.total);
            progress.progressbar('option', 'value', percentage);
        }
        return false;
    });

    $(xhr).bind("load", function(e){
        console.log('FileUpload: load event', e, xhr);
        progress.progressbar('option', 'value', 100);
        if (xhr.status != 200) {
            progress.addClass("error");
        }
        upload.uploading -= 1;
        if (upload.uploading==0) {
            $(upload.config.submitter).removeAttr('disabled');
        }
    });

    $(xhr.upload).bind("error", function(e){
        console.log('FileUpload: error event', e);
        progress.progressbar('option', 'value', 100);
        progress.addClass("error");
    });

    var boundary = "S-P-A-M----u-p-l-o-a-d--X30";


    var content = new String();
    content += '--' + boundary + '\r\n';
    content += 'Content-disposition: form-data;name="uploader"\r\n';
    content += '\r\n';
    content += '1';
    content += '\r\n';
    content += '--' + boundary + '\r\n';
    content += 'Content-Disposition: file; name="uploadfile"; filename="' + file.name + '"\r\n';
    content += 'Content-Type: ' + file.type + '\r\n';
    content += 'Content-Length: ' + fileData.length + '\r\n';
    content += '\r\n';
    content += fileData + '\r\n';
    content += '\r\n';
    content += '--' + boundary + '--\r\n';

    xhr.open("POST", upload.config.target);
    xhr.setRequestHeader('Content-Type', 'multipart/form-data; boundary=' + boundary);
    xhr.setRequestHeader('Content-Length', content.length);
    xhr.sendAsBinary(content);

}

upload.activate = function(uploader, config){
    if (typeof(config)=='undefined' || config==null) config = {};
    if (!('queue' in config)) config.queue = "#upload_queue";
    if (!('target' in config)) config.target = "/upload";
    if (!('submitter' in config)) config.submitter = ".submitbutton";
    if (!('ext' in config)) config.ext = "";
    upload.config = config;

    uploader.bind("dragenter", function(e) {
        return false;
    }).bind("dragover", function(e) {
        return false;
    }).bind("drop", function(e) {
        var dt = e.originalEvent.dataTransfer;
        upload.handle_files(upload.config.queue, dt.files);
        return false;
    });

    uploader.bind("change", function(e) {
        upload.handle_files(upload.config.queue, e.target.files);
        return false;
    });
}
