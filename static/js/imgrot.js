// Change the img1, img2 etc files to change the images u want to have in the left top corner they change every reload!
var imagesArray = [
    "/static/img/Emojies/KiraHeart.png",
    "/static/img/Emojies/KiraWow.png",
    "/static/img/Emojies/KiraWha.png",
    "/static/img/Emojies/KiraSob.png",
    "/static/img/Emojies/KiraSlurp.png",
    "/static/img/Emojies/Kirasend.png",
    "/static/img/Emojies/KiraPweas.png",
    "/static/img/Emojies/KiraPat.png",
    "/static/img/Emojies/KiraNpc.png",
    "/static/img/Emojies/KiraMad.png",
    "/static/img/Emojies/KiraLove.png",
    "/static/img/Emojies/KiraLook.png", 
    "/static/img/Emojies/KiraBlanky.png",//these can be replaced to the users likeing 
    "/static/img/Emojies/KiraHey.png"
];
var index = Math.floor(Math.random() * imagesArray.length);
document.write("<img src='" + imagesArray[index] + "' alt='Header Image' id='RotImg'>");