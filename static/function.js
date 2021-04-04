function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();

         reader.onload = function (e) {
             $('#blah').attr('src', e.target.result);
         }

     reader.readAsDataURL(input.files[0]);
    }
}

$("#input").change(function(){
    readURL(this);
    });

$("select#crypto").on("change", function(){
    var algo = $("#crypto").val();
    var html_v = '<div class="form-group"><label for="text">Enter delay:</label><input type="text" class="form-control" id="text" name="delay" placeholder="Enter delay for Vigenere cipher" required/><small>Enter text</small></div>';
    var html_c = '<div class="form-group"><label for="no">Enter delay:</label><input type="number" class="form-control" id="no" name="delay" placeholder="Enter delay for Caesar\'s cipher" min="1" max="26" pattern="^([1-9]|1[0-9]|2[0-6])$" required/><small>Enter numbers</small></div>';
    var desc_n = '<h3><strong>NONE</strong></h3><h4>You\'ve selected <strong>none</strong>. No cipher will be used.</h4>';
    var desc_v = '<h3><strong>VIGENERE\'S CIPHER</strong></h3><h4>Method of encrypting alphabetic text by using a series of interwoven Caesar ciphers based on the letters of a keyword. Though the \'chiffre indéchiffrable\' is easy to understand and implement, for three centuries it resisted all attempts to break it.</h4>';
    var desc_c = '<h3><strong>CAESAR\'S CIPHER</strong></h3><h4>Method in which each letter in the plaintext is replaced by a letter some fixed number of positions down the alphabet. The method is named after Julius Caesar, who used it in his private correspondence.</h4>';


    if(algo === 'none'){
        $("#delay").html('');
        $("#explain").html(desc_n);
    }else if (algo === 'vigenere') {
        $("#delay").html(html_v);
        $("#explain").html(desc_v);
    }else if (algo === 'caesar') {
        $("#delay").html(html_c);
        $("#explain").html(desc_c);
    }
});
