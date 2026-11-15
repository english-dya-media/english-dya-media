// english_dya - YouTube playlists
// Creates the channel's playlists and, every hour, puts each new public video into its playlist (chosen by its tags).
// Lives in the Apps Script project "english_dya YouTube playlists" (account of the channel); this file is its copy.
// Run setup() once: it checks the channel, creates the playlists and installs the hourly trigger.
// Needs the service "YouTube Data API v3" (identifier: YouTube).

var CHANNEL_ID = 'UCmaRj8tvAFXUgJICrLHcqXg';
var CUTOFF = '2026-11-14T00:00:00Z';  // only videos from the english_dya Shorts era; the 2023 clips stay out
// One playlist per format and per story series (series playlists are made when their first part is out).
// A video goes to the first playlist whose tag it carries (tags come from studio/youtube.py); no match -> the last one.
var PLAYLISTS = [
  {key: "rostam", tag: "rostam and sohrab", eager: true, title: "\ud83c\udfac \u0631\u0633\u062a\u0645 \u0648 \u0633\u0647\u0631\u0627\u0628 | Shahnameh in English",
   description: "\u062f\u0627\u0633\u062a\u0627\u0646 \u0631\u0633\u062a\u0645 \u0648 \u0633\u0647\u0631\u0627\u0628 \u0627\u0632 \u0634\u0627\u0647\u0646\u0627\u0645\u0647\u200c\u06cc \u0641\u0631\u062f\u0648\u0633\u06cc\u060c \u0628\u0647 \u0627\u0646\u06af\u0644\u06cc\u0633\u06cc \u0628\u0627 \u0632\u06cc\u0631\u0646\u0648\u06cc\u0633 \u0641\u0627\u0631\u0633\u06cc. \u0647\u0631 \u0631\u0648\u0632 \u062f\u0648 \u0642\u0633\u0645\u062a \u062a\u0627\u0632\u0647."},
  {key: "babak", tag: "babak khorramdin", title: "\ud83c\udfac \u0628\u0627\u0628\u06a9 \u062e\u0631\u0645\u062f\u06cc\u0646 | Babak Khorramdin in English",
   description: "\u062f\u0627\u0633\u062a\u0627\u0646 \u0628\u0627\u0628\u06a9 \u062e\u0631\u0645\u062f\u06cc\u0646 \u0628\u0647 \u0627\u0646\u06af\u0644\u06cc\u0633\u06cc \u0628\u0627 \u0632\u06cc\u0631\u0646\u0648\u06cc\u0633 \u0641\u0627\u0631\u0633\u06cc\u060c \u0642\u0633\u0645\u062a \u0628\u0647 \u0642\u0633\u0645\u062a."},
  {key: "zahhak", tag: "zahhak", title: "\ud83c\udfac \u0636\u062d\u0627\u06a9 \u0648 \u0641\u0631\u06cc\u062f\u0648\u0646 | Zahhak & Fereydun in English",
   description: "\u062f\u0627\u0633\u062a\u0627\u0646 \u0636\u062d\u0627\u06a9 \u0648 \u0641\u0631\u06cc\u062f\u0648\u0646 \u0628\u0647 \u0627\u0646\u06af\u0644\u06cc\u0633\u06cc \u0628\u0627 \u0632\u06cc\u0631\u0646\u0648\u06cc\u0633 \u0641\u0627\u0631\u0633\u06cc\u060c \u0642\u0633\u0645\u062a \u0628\u0647 \u0642\u0633\u0645\u062a."},
  {key: "arash", tag: "arash the archer", title: "\ud83c\udfac \u0622\u0631\u0634 \u06a9\u0645\u0627\u0646\u06af\u06cc\u0631 | Arash the Archer in English",
   description: "\u062f\u0627\u0633\u062a\u0627\u0646 \u0622\u0631\u0634 \u06a9\u0645\u0627\u0646\u06af\u06cc\u0631 \u0628\u0647 \u0627\u0646\u06af\u0644\u06cc\u0633\u06cc \u0628\u0627 \u0632\u06cc\u0631\u0646\u0648\u06cc\u0633 \u0641\u0627\u0631\u0633\u06cc\u060c \u0642\u0633\u0645\u062a \u0628\u0647 \u0642\u0633\u0645\u062a."},
  {key: "leyli", tag: "layla and majnun", title: "\ud83c\udfac \u0644\u06cc\u0644\u06cc \u0648 \u0645\u062c\u0646\u0648\u0646 | Leyli & Majnun in English",
   description: "\u062f\u0627\u0633\u062a\u0627\u0646 \u0644\u06cc\u0644\u06cc \u0648 \u0645\u062c\u0646\u0648\u0646 \u0628\u0647 \u0627\u0646\u06af\u0644\u06cc\u0633\u06cc \u0628\u0627 \u0632\u06cc\u0631\u0646\u0648\u06cc\u0633 \u0641\u0627\u0631\u0633\u06cc\u060c \u0642\u0633\u0645\u062a \u0628\u0647 \u0642\u0633\u0645\u062a."},
  {key: "khosrow", tag: "khosrow and shirin", title: "\ud83c\udfac \u062e\u0633\u0631\u0648 \u0648 \u0634\u06cc\u0631\u06cc\u0646 | Khosrow & Shirin in English",
   description: "\u062f\u0627\u0633\u062a\u0627\u0646 \u062e\u0633\u0631\u0648 \u0648 \u0634\u06cc\u0631\u06cc\u0646 \u0628\u0647 \u0627\u0646\u06af\u0644\u06cc\u0633\u06cc \u0628\u0627 \u0632\u06cc\u0631\u0646\u0648\u06cc\u0633 \u0641\u0627\u0631\u0633\u06cc\u060c \u0642\u0633\u0645\u062a \u0628\u0647 \u0642\u0633\u0645\u062a."},
  {key: "hasan", tag: "\u062d\u0633\u0646 \u06a9\u0686\u0644", title: "\ud83c\udfac \u062d\u0633\u0646 \u06a9\u0686\u0644 | Hasan Kachal in English",
   description: "\u062f\u0627\u0633\u062a\u0627\u0646 \u062d\u0633\u0646 \u06a9\u0686\u0644 \u0628\u0647 \u0627\u0646\u06af\u0644\u06cc\u0633\u06cc \u0628\u0627 \u0632\u06cc\u0631\u0646\u0648\u06cc\u0633 \u0641\u0627\u0631\u0633\u06cc\u060c \u0642\u0633\u0645\u062a \u0628\u0647 \u0642\u0633\u0645\u062a."},
  {key: "mahpishani", tag: "persian cinderella", title: "\ud83c\udfac \u0645\u0627\u0647\u200c\u067e\u06cc\u0634\u0648\u0646\u06cc | Mah Pishani in English",
   description: "\u062f\u0627\u0633\u062a\u0627\u0646 \u0645\u0627\u0647\u200c\u067e\u06cc\u0634\u0648\u0646\u06cc \u0628\u0647 \u0627\u0646\u06af\u0644\u06cc\u0633\u06cc \u0628\u0627 \u0632\u06cc\u0631\u0646\u0648\u06cc\u0633 \u0641\u0627\u0631\u0633\u06cc\u060c \u0642\u0633\u0645\u062a \u0628\u0647 \u0642\u0633\u0645\u062a."},
  {key: "quote", tag: "english quotes", eager: true, title: "\ud83e\udd0d \u062c\u0645\u0644\u0627\u062a \u0627\u0646\u06af\u0644\u06cc\u0633\u06cc \u0628\u0627 \u062a\u0631\u062c\u0645\u0647",
   description: "\u0647\u0631 \u0634\u0628 \u06cc\u0647 \u062c\u0645\u0644\u0647\u200c\u06cc \u06a9\u0648\u062a\u0627\u0647 \u0627\u0646\u06af\u0644\u06cc\u0633\u06cc \u0628\u0627 \u0645\u0639\u0646\u06cc \u0641\u0627\u0631\u0633\u06cc."},
  {key: "trial", tag: "english mistakes", eager: true, title: "\ud83d\udde3\ufe0f \u0627\u0634\u062a\u0628\u0627\u0647\u0627\u062a \u0631\u0627\u06cc\u062c \u0648 \u0644\u063a\u062a\u200c\u0647\u0627\u06cc \u062d\u0631\u0641\u0647\u200c\u0627\u06cc",
   description: "\u062c\u0645\u0644\u0647\u200c\u0647\u0627\u06cc\u06cc \u06a9\u0647 \u0641\u0627\u0631\u0633\u06cc\u200c\u0632\u0628\u0627\u0646\u200c\u0647\u0627 \u0627\u0634\u062a\u0628\u0627\u0647 \u0645\u06cc\u200c\u06af\u0646 \u0648 \u06a9\u0644\u0645\u0647\u200c\u0647\u0627\u06cc\u06cc \u06a9\u0647 \u0627\u0646\u06af\u0644\u06cc\u0633\u06cc\u200c\u0627\u062a \u0631\u0648 \u062d\u0631\u0641\u0647\u200c\u0627\u06cc\u200c\u062a\u0631 \u0645\u06cc\u200c\u06a9\u0646\u0646."},
  {key: "reel", tag: null, eager: true, title: "\ud83d\udd0a \u062a\u0644\u0641\u0638 \u062f\u0631\u0633\u062a \u0644\u063a\u062a\u200c\u0647\u0627\u06cc \u0627\u0646\u06af\u0644\u06cc\u0633\u06cc",
   description: "\u0647\u0631 \u0631\u0648\u0632 \u06f4 \u06a9\u0644\u0645\u0647\u200c\u06cc \u0627\u0646\u06af\u0644\u06cc\u0633\u06cc \u0628\u0627 \u062a\u0644\u0641\u0638 \u062f\u0631\u0633\u062a \u0648 \u0645\u0639\u0646\u06cc \u0641\u0627\u0631\u0633\u06cc."}
];

function setup() {
  var ch = YouTube.Channels.list('id,snippet', {mine: true}).items || [];
  if (!ch.length || ch[0].id !== CHANNEL_ID) {
    throw new Error('Wrong channel: ' + (ch.length ? ch[0].snippet.title + ' ' + ch[0].id : 'none') + '. Authorize with the english_dya channel.');
  }
  ensurePlaylists_();
  ScriptApp.getProjectTriggers().forEach(function (t) {
    if (t.getHandlerFunction() === 'sortNewVideos') ScriptApp.deleteTrigger(t);
  });
  ScriptApp.newTrigger('sortNewVideos').timeBased().everyHours(1).create();
  sortNewVideos();
}

function ensurePlaylists_() {
  var props = PropertiesService.getScriptProperties();
  var ids = JSON.parse(props.getProperty('playlists') || '{}');
  var existing = {}, token = null;
  do {
    var r = YouTube.Playlists.list('snippet', {mine: true, maxResults: 50, pageToken: token});
    (r.items || []).forEach(function (p) { existing[p.snippet.title] = p.id; });
    token = r.nextPageToken;
  } while (token);
  var known = Object.keys(existing).map(function (k) { return existing[k]; });
  PLAYLISTS.forEach(function (p) {
    if (ids[p.key] && known.indexOf(ids[p.key]) >= 0) return;
    delete ids[p.key];
    if (existing[p.title]) ids[p.key] = existing[p.title];
    else if (p.eager) ids[p.key] = makePlaylist_(p);
  });
  props.setProperty('playlists', JSON.stringify(ids));
  return ids;
}

function makePlaylist_(p) {
  return YouTube.Playlists.insert({snippet: {title: p.title, description: p.description, defaultLanguage: 'fa'},
                                   status: {privacyStatus: 'public'}}, 'snippet,status').id;
}

function playlistFor_(p, ids) {  // a series playlist is made the first time one of its parts comes out
  if (!ids[p.key]) {
    ids[p.key] = makePlaylist_(p);
    PropertiesService.getScriptProperties().setProperty('playlists', JSON.stringify(ids));
  }
  return ids[p.key];
}

function sortNewVideos() {
  var props = PropertiesService.getScriptProperties();
  var ids = ensurePlaylists_();
  var done = JSON.parse(props.getProperty('done') || '[]');
  var uploads = YouTube.Channels.list('contentDetails', {mine: true}).items[0].contentDetails.relatedPlaylists.uploads;
  var fresh = [], token = null;
  do {
    var r = YouTube.PlaylistItems.list('contentDetails', {playlistId: uploads, maxResults: 50, pageToken: token});
    (r.items || []).forEach(function (it) {
      var v = it.contentDetails.videoId;
      if (done.indexOf(v) < 0) fresh.push(v);
    });
    token = r.nextPageToken;
  } while (token && fresh.length < 150);
  fresh.reverse();  // oldest first, so series parts land in order
  var added = 0;
  for (var i = 0; i < fresh.length; i += 50) {
    var chunk = fresh.slice(i, i + 50), byId = {};
    (YouTube.Videos.list('snippet,status', {id: chunk.join(',')}).items || []).forEach(function (v) { byId[v.id] = v; });
    chunk.forEach(function (id) {
      var v = byId[id];
      if (!v || v.status.privacyStatus !== 'public') return;  // not published yet: next hour
      if (v.snippet.publishedAt < CUTOFF) { done.push(id); return; }  // old upload: never sorted
      var tags = (v.snippet.tags || []).map(function (t) { return t.toLowerCase(); });
      var p = PLAYLISTS.filter(function (p) { return p.tag && tags.indexOf(p.tag) >= 0; })[0] || PLAYLISTS[PLAYLISTS.length - 1];
      YouTube.PlaylistItems.insert({snippet: {playlistId: playlistFor_(p, ids), resourceId: {kind: 'youtube#video', videoId: id}}}, 'snippet');
      done.push(id);
      added++;
    });
  }
  props.setProperty('done', JSON.stringify(done.slice(-3000)));
  console.log(added + ' video(s) added to playlists');
}

// One-off: take uploads from before CUTOFF out of our playlists (the first run sorted the 2023 clips too).
function removeOldFromPlaylists() {
  var ids = ensurePlaylists_(), removed = 0;
  Object.keys(ids).forEach(function (k) {
    var token = null, old = [];
    do {
      var r = YouTube.PlaylistItems.list('contentDetails', {playlistId: ids[k], maxResults: 50, pageToken: token});
      (r.items || []).forEach(function (it) {
        var at = it.contentDetails.videoPublishedAt;
        if (at && at < CUTOFF) old.push(it.id);
      });
      token = r.nextPageToken;
    } while (token);
    old.forEach(function (itemId) { YouTube.PlaylistItems.remove(itemId); removed++; });
  });
  console.log(removed + ' old video(s) removed from playlists');
}
