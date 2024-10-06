username='velarde_jocelyn'
password='Ffcd5D4E1o'
let headers = new Headers();
headers.set('Authorization', 'Basic ' + btoa(username + ":" + password));

fetch('https://login.meteomatics.com/api/v1/token', {
    method: 'GET', headers: headers
}).then(function (resp) {
    return resp.json();
}).then(function (data) {
    var token = data.access_token;
    console.log('token', token);
}).catch(function (err) {
    console.log('something went wrong', err);
});