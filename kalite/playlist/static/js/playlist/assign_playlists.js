function appendStudentGrp(id, studentGrp) {
  $("#student-grps-" + id + " ul").append('<li>'+studentGrp+'</li>');
}
function allowDrop(ev) {
  ev.preventDefault();
}

function drag(ev) {
  var target = ev.currentTarget;
  var studentGrp = target.innerText || target.textContent;
  ev.originalEvent.dataTransfer.setData('student-grp', studentGrp);
}

function drop(ev) {
  var array = ev.currentTarget.id.split('-');
  var length = array.length;
  var id = array[length - 1];
  ev.preventDefault();
  var studentGrp = ev.originalEvent.dataTransfer.getData('student-grp');
  appendStudentGrp(id, studentGrp);
}

// modify the groups assigned to a playlist
function api_modify_groups(playlist_id, group_ids_assigned) {
  var PLAYLIST_DETAIL_URL = ALL_PLAYLISTS_URL + playlist_id + "/"; // note: cleanup to something more readable
  var groups_assigned = group_ids_assigned.map(function (id) { return {"id": id}; });
  doRequest(PLAYLIST_DETAIL_URL,
            {"groups_assigned": groups_assigned},
            {"dataType": "text", // use text so jquery doesn't do the error callback since the server returns an empty response body
             "type": "PATCH"}).success(function() {
               clear_messages();
              show_message("success", gettext("Successfully updated playlist groups."));
            }).error(function(e) {
              if (e.status === 404) {
                clear_messages();
                show_message("error", gettext("That playlist cannot be found."));
              }
            });
}


// get and display all groups
$(function() {
    doRequest(ALL_GROUPS_URL).success(function(data) {
        data.objects.map(function(obj) {
            $("table[id|=all-student-groups] tr:last").after(sprintf('<tr><td>%(name)s</td></tr>', obj));
        });
    });
});

// get and display all playlists and their assigned groups
$(function() {
    doRequest(ALL_PLAYLISTS_URL).success(function(data) {
        data.objects.map(function(playlist) {
            $("table[id|=playlist-table] tr:last").after(sprintf("<tr class='playlist-title' playlist_id='%(id)s'><td>%(title)s</td></tr>", playlist));
            $("tr[class|=playlist-title]:last").after("<tr class='playlist-groups-assigned'><td><ul></ul></td></tr>");

            playlist.groups_assigned.map(function(group) {
                $("tr[class|=playlist-groups-assigned]:last ul").append(sprintf("<li group_id='%(id)s'>%(name)s</li>", group));
            });
        });
    });
});

$(function() {
    $(".span3 td").on('dragstart', drag);
    $("tr[id|=student-grps]").on('dragover', allowDrop);
    $("tr[id|=student-grps]").on('drop', drop);
    $("tr[id|=title]").on('dragover', allowDrop);
    $("tr[id|=title]").on('drop', drop);
    $("tr[id|=student-grps]").hide();
    $("tr[id|=title]").click(function(e) {
        var target = e.target;
        var targetId = e.currentTarget.id;
        var idNum = targetId.split('-')[1];
        $("#student-grps-" + idNum).toggle();
    });
});