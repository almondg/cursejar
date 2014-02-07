(function($){

    $.fn.autoGrowInput = function(o) {

        o = $.extend({
            maxWidth: 1000,
            minWidth: 0,
            comfortZone: 70
        }, o);

        this.filter('input:text').each(function(){

            var minWidth = o.minWidth || $(this).width(),
                // Note: I changed this from '' to undefined so the adjusting will be called
                // at least once (for empty inputs) (user4 @ 2013-04-21)
                val = undefined,
                input = $(this),
                testSubject = $('<editabletext/>').css({
                    position: 'absolute',
                    top: -9999,
                    // Note: I changed this from left to right so it would work
                    // well in rtl (user4 @ 2013-04-23)
                    right: -9999,
                    width: 'auto',
                    fontSize: input.css('fontSize'),
                    fontFamily: input.css('fontFamily'),
                    fontWeight: input.css('fontWeight'),
                    letterSpacing: input.css('letterSpacing'),
                    whiteSpace: 'nowrap'
                }),
                check = function() {

                    if (val === input.val()) {
                        return;
                    }
                    val = input.val();

                    // Enter new content into testSubject
                    var escaped = val.replace(/&/g, '&amp;').replace(/(\s)\s/g,'$1&nbsp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
                    testSubject.html(escaped);

                    // Calculate new width + whether to change
                    var testerWidth = testSubject.width(),
                        newWidth = (testerWidth + o.comfortZone) >= minWidth ? testerWidth + o.comfortZone : minWidth,
                        currentWidth = input.width(),
                        isValidWidthChange = (newWidth < currentWidth && newWidth >= minWidth)
                                             || (newWidth > minWidth && newWidth < o.maxWidth);

                    // Animate width
                    if (isValidWidthChange) {
                        input.width(newWidth);
                    }

                };

            testSubject.insertAfter(input);

            $(this).bind('keyup keydown blur update', check);

        });

        return this;

    };

})(jQuery);