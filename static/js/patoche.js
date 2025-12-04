document.addEventListener("DOMContentLoaded", () => {
    const input = document.getElementById('msg');
    const chat = document.getElementById('chat');

    if (input) {
        input.focus();
    }

    function appendUserMessage(msg) {
        chat.innerHTML += `
            <div class="message-bubble self-end max-w-[80%] rounded-2xl bg-indigo-500 text-xs sm:text-sm text-slate-50 shadow-lg px-3 py-2 ml-auto">
                <div class="text-[0.65rem] uppercase tracking-wide text-indigo-100/80 mb-0.5">Toi</div>
                <div>${msg}</div>
            </div>
        `;
    }

    function appendPatocheMessage(text) {
        chat.innerHTML += `
            <div class="message-bubble max-w-[80%] rounded-2xl bg-slate-800/95 border border-slate-700 text-xs sm:text-sm text-slate-100 shadow-lg px-3 py-2">
                <div class="text-[0.65rem] uppercase tracking-wide text-slate-400 mb-0.5">Patoche</div>
                <div>${text}</div>
            </div>
        `;
    }

    window.send = function() {
        let msg = input.value.trim();
        if (!msg) return;

        appendUserMessage(msg);

        fetch(`/ask/?msg=${encodeURIComponent(msg)}`)
            .then(r => r.json())
            .then(data => {
                appendPatocheMessage(data.reponse);
                chat.scrollTop = chat.scrollHeight;
            })
            .catch(() => {
                appendPatocheMessage(
                    "Attends j’ai renversé mon pastaga sur le clavier… Recommence, p’tit malin !"
                );
                chat.scrollTop = chat.scrollHeight;
            });

        input.value = "";
        chat.scrollTop = chat.scrollHeight;
    };

    if (input) {
        input.addEventListener('keypress', e => {
            if (e.key === 'Enter') send();
        });
    }
});
