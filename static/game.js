function autocomplete(inp) {
    var currentFocus;
    let hints_enabled = get_cookie("hintsenabled", false);
    inp.addEventListener("input", function(e) {
        var a, b, i, val = this.value;
        close_all_lists();
        if(!val) {return false;}
        currentFocus = -1;
        a = document.createElement("DIV");
        a.setAttribute("id", this.id + "autocomplete-list");
        a.setAttribute("class", "autocomplete-items");
        this.parentNode.appendChild(a);
        // Search function
        for(const [key, value] of Object.entries(items)) {
            let key_up = key.toUpperCase();
            let search_up = val.toUpperCase();
            let search_words = search_up.split(" ");
            let matches = key.includes(val)? 1:0;
            // Searching awp asii should only show awp asiimov, not other asiimov skins
            let all_words_fit = true;
            for(i = 0; i < search_words.length; i++) {
                // If at any point we do not have a found search word, move on
                if(!key_up.includes(search_words[i])) {
                    all_words_fit = false;
                    continue
                }
                else {
                    matches++;
                }
            }
            if(matches > 0 && all_words_fit) {
                // Highlight matched substring using <strong>
                key_highlight = "";
                searched_terms = [];
                highlight_indices = [];
                for(i = 0; i < search_words.length; i++) {
                    search_word = search_words[i];
                    if(searched_terms.includes(search_word)) {
                        continue
                    }
                    search_split = key_up.split(search_words[i]);
                    for(let j = 0; j < key_up.length + 1 - search_word.length; j++) {
                        if(key_up.substring(j, j + search_word.length) === search_word) {
                            highlight_indices.push({
                                "start": j,
                                "end": j + search_word.length
                            });
                        }
                    }
                    searched_terms.push(search_word)
                }
                // Now we go look at the start and end indices and combine where possible
                let sorted_indices = highlight_indices.sort((a, b) => a["start"] > b["start"] ? 1:-1);
                let merged = [];
                for(i = 0; i < sorted_indices.length; i++) {
                    let len_merged = merged.length;
                    if(len_merged == 0 || merged[len_merged - 1]['end'] < sorted_indices[i]['start']) {
                        merged.push(sorted_indices[i]);
                    }
                    else {
                        merged[len_merged - 1]['end'] = Math.max(merged[len_merged - 1]['end'], sorted_indices[i]['end']);
                    }
                }
                let highlighted_word = ""
                // We now loop through merged and add <strong>s throughout
                if(merged[0]["start"] > 0) {
                    highlighted_word += key.substring(0, merged[0]["start"]);
                }
                for(i = 0; i < merged.length; i++) {
                    start = merged[i]["start"];
                    end = merged[i]["end"];
                    highlighted_word += "<strong>" + key.substring(start, end) + "</strong>";
                    if(merged[i + 1]) {
                        highlighted_word += key.substring(end, merged[i+1]["start"]);
                    }
                }
                // Highlight whatever's left
                highlighted_word += key.substring(merged[merged.length - 1]["end"], key.length);
                b = document.createElement("DIV");
                color_hex = value['rarity_color'];
                b.innerHTML = `<p style='color:#${color_hex};'>${highlighted_word}</p>`
                if(hints_enabled == "1" | hints_enabled == "") {
                    let weapon_type = value['weapon_category'];
                    let avg_price = format_price(value['avg_price']);
                    let highest_price = format_price(value['highest_price']);
                    b.innerHTML += "<span class=\"dropinfo\"> Category: " + weapon_type + 
                        ", Average Price: $"+avg_price + ", Highest Price: $" +highest_price + "</span>";
                }
                b.innerHTML += "<input type='hidden' value='" + value + "'>";
                b.addEventListener("click", function(e) {
                    inp.value = key;
                    close_all_lists();
                });
                a.appendChild(b);
            }
        }
    });

    inp.addEventListener("keydown", function(e) {
        var x = document.getElementById(this.id + "autocomplete-list");
        if (x) x = x.getElementsByTagName("div");
        if (e.keyCode == 40) {
            currentFocus++;
            addActive(x);
        }
        else if (e.keyCode == 38) {
            currentFocus--;
            addActive(x);
        }
        else if(e.keyCode == 13) {
            e.preventDefault();
            if(currentFocus > -1) {
                if (x) x[currentFocus].click();
            }
        }
    });

    function addActive(x) {
        if (!x) return false;
        removeActive(x);
        if (currentFocus >= x.length) currentFocus = 0;
        if (currentFocus< 0) currentFocus = (x.length - 1);
        x[currentFocus].classList.add("autocomplete-active");
    }

    function removeActive(x) {
        for (var i = 0; i < x.length; i++) {
            x[i].classList.remove("autocomplete-active");
        }
    }
    
    function close_all_lists(element) {
        var x = document.getElementsByClassName("autocomplete-items");
        for(var i = 0; i < x.length; i++) {
            if(element != x[i] && element != inp) {
                x[i].parentNode.removeChild(x[i]);
            }
        }
    }

    document.addEventListener("click", function(e) {
        close_all_lists(e.target);
    });
}

function format_price(price) {
    txt = price.toString();
    if(txt.includes(".")) {
        txt_split = txt.split(".");
        if(txt_split[1].length < 2) {
            for(let j = 0; j < txt_split[1].length; j++) {
                txt += "0";
            }
        }
        return txt;
    }
    else {
        return txt + ".00";
    }
}

function set_cookie(cookie_name, cookie_value, ex, daily) {
    cookie_name = (daily?"d_":"") + cookie_name;
    const d = new Date();
    if (daily) {
        d.setTime(d.getTime() + (24*60*60*1000));
        d.setUTCHours(10);
        d.setMinutes(0);
        d.setSeconds(0);
    }
    else {
        d.setTime(d.getTime() + (ex*24*60*60*1000));
    }
    let expires = "expires=" + d.toUTCString();
    document.cookie = cookie_name + "=" + cookie_value + ";" + expires + ";path=/"+";samesite=strict";
}

function get_cookie(cookie_name, daily) {
    cookie_name = (daily?"d_":"") + cookie_name;
    var cookies = `${document.cookie}`.split(";");
    for(var i = 0; i < cookies.length; i++) {
        var cookie = cookies[i].split("=");
        if(cookie[0].trim() == `${cookie_name}`) {
            return cookie[1];
        }
    }
    return "";
}

let createElement = (initObj) => {
    var element = document.createElement(initObj.Tag);
    for (var prop in initObj) {
        if (prop === "childNodes") {
            initObj.childNodes.forEach(function (node) {element.appendChild(node); });
        }
        else if (prop === "attributes") {
            initObj.attributes.forEach(function (attr) {element.setATtribute(attr.key, attr.value); });
        }
        else element[prop] = initObj[prop];
    }
    return element;
}

function show_state(daily) {
    let enabled = get_cookie("hintsenabled", false);
    document.getElementById("toggleinfo").innerHTML = "📋 Skin Info " + (enabled=="0"?"OFF":"ON");
    let guesses = get_cookie("guesses_2", daily);
    let attempts = get_cookie("t_attempts", daily);
    guesses = guesses == ""? []:JSON.parse(guesses);
    let guesses_cont = document.getElementById("guesses");
    let hint_titles = document.getElementById("hinttitles");

    if (guesses.length > 0) {
        if (guesses_cont.style.display == "none") {
            guesses_cont.style.display = "block";
            window.getComputedStyle(hint_titles).opacity;
            hint_titles.className += ' in';
        }
    }
    else {
        guesses_cont.style.display = "none";
        hint_titles.className = 'row';
    }
    let last_attempt = "";
    for (const [index, guess] of guesses.entries()) {
        if (!(document.getElementById('guess'+index) || false)) {
            last_attempt = guess.guess_name + "///" + guess.guess_exterior;
            var rowElement = createElement({Tag:"div", id:"guess"+index, classList:'row'});
            for (const hint of guess.hints) {
                var img = createElement({Tag:"img", classList:"emoji", src:hint});
                var colElement = createElement({Tag:"div", classList:"column", childNodes:[img]});
                rowElement.appendChild(colElement);
            }
            let col = "color: #" + items[guess.guess_name]["rarity_color"] + ";"
            let full_guess = guess.guess_name + " (" + guess.guess_exterior + ")";
            var item_info = createElement({Tag:"span", classList:"tooltiptext",
                innerHTML:`<p style='${col}'>`+full_guess+"</p>" + guess.info});
            var item_thumb = createElement({Tag:"img",alt:guess.guess_name, 
                classList:"item_thumb", src:items[guess.guess_name]["exterior"][guess.guess_exterior]["url"]});
            var tooltip = createElement({Tag:"div", classList:"tooltip", childNodes:[item_info, item_thumb]});
            var colElement = createElement({Tag:"div", classList:"column", childNodes:[tooltip]});
            rowElement.appendChild(colElement);
            guesses_cont.appendChild(rowElement);
            window.getComputedStyle(rowElement).opacity;
            rowElement.classname += ' in';
        }
    }
    let secret_name = get_cookie("secret_item", daily).replace(/"/g, '');
    if (secret_name == last_attempt) {
        document.getElementById("guessform").style.display = "none";
        document.getElementById("results").style.display = "block";
        document.getElementById("won").style.display = "block";
    }
    else if (guesses.length == attempts) {
        document.getElementById("guessform").style.display = "none";
        document.getElementById("results").style.display = "block";
        document.getElementById("lost").style.display = "block";
        document.getElementById("secret_thumb").style.display = "block";
    }
    document.getElementById("attempts").innerHTML = attempts-guesses.length;
}

function handle_guess(daily, im1, im2, im3, im4) {
    // 1 = correct, 2 = up, 3 = down, 4 = wrong
    const imgs = {'1': im1, "2": im2, "3": im3, "4": im4};
    let guess_name = document.getElementById("guess_weapon").value;
    let guess_exterior = document.getElementById("guess_exterior").value;
    // Format is skin///ext
    let secret_split = get_cookie("secret_item", daily).replace(/"/g, '').split("///");
    let guess = items[guess_name];
    if (guess == null) {
        document.getElementById("error_name").style.display = "block";
        return
    }
    // If guess is found but exterior is not
    else if (guess["exterior"][guess_exterior] == null) {
        document.getElementById("error_exterior").style.display = "block";
        return
    }
    document.getElementById("error_name").style.display = "none";
    document.getElementById("error_exterior").style.display = "none";
    document.getElementById("guess_weapon").value = "";

    let secret = items[secret_split[0]];
    // Object used to compare condition
    let exteriors = {
        "Factory New": 4,
        "Minimal Wear": 3,
        "Field-Tested": 2,
        "Well-Worn": 1,
        "Battle-Scarred": 0
    }
    let rarities = {
        "Consumer Grade": 0,
        "Industrial Grade": 1,
        "Mil-Spec Grade": 2,
        "Restricted": 3,
        "Classified": 4,
        "Covert": 5,
        "Contraband": 6
    }
    let guess_paint = guess_name.split("|")[1].trim();
    let secret_paint = secret_split[0].split("|")[1].trim();
    let category = guess["weapon_category"] == secret["weapon_category"]? "1":"4";
    let weapon_name = guess["weapon_class"] == secret["weapon_class"]? "1": "4";
    let paint = guess_paint == secret_paint? "1": "4";
    let price = guess["exterior"][guess_exterior]["price"] == secret["exterior"][secret_split[1]]["price"]? "1":
        guess["exterior"][guess_exterior]["price"] < secret["exterior"][secret_split[1]]["price"] ? "2":"3";
    let rarity = guess["rarity"] == secret["rarity"]? "1":
        rarities[guess["rarity"]] < rarities[secret["rarity"]]? "2": "3";
    let exterior = guess_exterior == secret_split[1] ? "1": 
        exteriors[guess_exterior] < exteriors[secret_split[1]]? "2":"3";
    
    let item_info = "<b>Category: </b>" + guess["weapon_category"]+"<br><b>Price: </b>$"
    item_info += format_price(guess["exterior"][guess_exterior]["price"]) + "<br><b>Rarity: </b>"
    item_info += guess["rarity"];
    
    let guess_info = {
        "hints":[imgs[category], imgs[weapon_name], imgs[paint], imgs[price], imgs[rarity], imgs[exterior]],
        "guess_name": guess_name,
        "guess_exterior": guess_exterior,
        "info": item_info,
        "mosaic": category + weapon_name + paint + price + rarity + exterior
    }

    let guesses = get_cookie("guesses_2", daily);
    guesses = guesses == ""? []:JSON.parse(guesses)
    guesses.push(guess_info)

    set_cookie("guesses_2", JSON.stringify(guesses), 100, daily)
    show_state(daily)
}

function replace_at(str,index,ch) {
    return str.replace(/./g, (c,i) => i == index ? ch:c);
}

function copy_current_day(day, names) {
    let attempts = parseInt(get_cookie("t_attempts", day > -1));
    var guesses = JSON.parse(get_cookie("guesses_2", day > -1));
    var g_len = guesses.length;
    if (document.getElementById('lost').style.display == "block") {
        g_len = "X"
    }
    var daily_info = day == -1?"":("Daily "+ day + " - ");
    var text = "";
    for (const guess of guesses) {
        let mosaic = guess.mosaic;
        if (day > -1 & (mosaic[0] == "2" | mosaic[0] == "3")) {
            mosaic = replace_at(mosaic, 0, '6');
        }
        text = text + "\n" + mosaic;
    }
    text = text.replace(/1/g, '🟩');
    text = text.replace(/2/g, '🔼');
    text = text.replace(/3/g, '🔽');
    text = text.replace(/4/g, '🟥');
    let mosaic_daily = "";
    if (day > -1) {mosaic_daily = "/daily"}

    text = "CS:GOrdle " + daily_info + g_len + "/" + attempts + text + "\n\ncsgordle.holla.one" + mosaic_daily;
    var success = "Copied results to clipboard!"
    if (window.clipboardData && window.clipBoardData.setData) {
        alert(success);
        return clipBoardData.setData("Text", text);
    }
    else if (document.queryCommandSupported && document.queryCommandSupported("copy")) {
        var textarea = document.createElement("textarea");
        textarea.textContent = text;
        textarea.style.position = "fixed";
        document.body.appendChild(textarea);
        textarea.select();
        try {
            return document.execCommand("copy");
        } catch (ex) {
            console.warn("Copy to clipboard failed. Let holla know!", ex);
            return false;
        } finally {
            document.body.removeChild(textarea);
            alert(success);
        }
    }
}

function toggle_hints(daily) {
    let enabled = get_cookie("hintsenabled", false);
    enabled = enabled == "0"? "1":"0";
    set_cookie("hintsenabled", enabled);
    document.getElementById("toggleinfo").innerHTML = "📋 Skin Info " + (enabled=="1"?"ON":"OFF");
    autocomplete(document.getElementById("guess_weapon"));
}

function get_skin() {
    len_items = Object.keys(items).length;
    let chosen_name = Object.keys(items)[len_items * Math.random() | 0];
    let len_exteriors = Object.keys(items[chosen_name]["exterior"]).length;
    let chosen_exterior = Object.keys(items[chosen_name]["exterior"])[len_exteriors * Math.random() | 0];
    skin = {
        "name": chosen_name,
        "exterior": chosen_exterior
    }
    return skin;
}

function new_game(daily) {
    let secret_skin = "";
    let secret_present_skin = "";
    set_cookie("guesses_2","", 30,daily);
    set_cookie("t_attempts", 8, 30,daily);
    skin = get_skin();
    secret_skin = skin["name"] + "///" + skin["exterior"];
    secret_present_skin = skin["name"] + " (" + skin["exterior"] + ")"
    set_cookie("secret_item",  secret_skin, 30,daily);
    set_cookie("secret_present",  secret_present_skin, 30,daily);
    autocomplete(document.getElementById("guess_weapon"));

    for (x in [0,1,2,3,4,5,6,7]) {
        const elem = document.getElementById("guess"+x) || false;
        elem?elem.remove():false;
    }

    document.getElementById("guessform").style.display = "block";
    document.getElementById("results").style.display = "none";
    document.getElementById("skinhint_text").style.display = "none";
    document.getElementById("lost").style.display = "none";
    document.getElementById("won").style.display = "none";
    document.getElementById("secretskin").innerHTML = secret_present_skin;
    document.getElementById("secret_thumb").src = items[skin["name"]]["exterior"][skin["exterior"]]["url"];
    show_state(daily);

}

// Shows a hint for the secret skin, containing info on what side wep it is as well as category
function show_hint(daily) {
    // If not ct or t, they're shared
    let ct = ["five-seven", "p2000", "usp-s", "mag-7", "mp9", "aug", "famas", "m4a1-s", "m4a4", "scar-20"]
    let t = ["glock-18", "tec-9", "sawed-off", "mac-10", "ak-47", "galil ar", "sg 553", "g3sg1"]
    let secret_split = get_cookie("secret_item", daily).replace(/"/g, '').split("///");
    let secret_class_lower = items[secret_split[0]]['weapon_class'].toLowerCase();
    let secret_category = items[secret_split[0]]['weapon_category'];
    let hint = `Category: ${secret_category}, Side: `
    if (ct.includes(secret_class_lower)) {
        hint += 'CT'
    }
    else if (t.includes(secret_class_lower)) {
        hint += 'T'
    }
    else {
        hint += 'Both CT & T'
    }
    let hint_element = document.getElementById('skinhint_text');
    hint_element.style.display = "block";
    hint_element.innerHTML = hint;
}