#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 13 14:49:04 2022

__author__ = "Simen Roko Krogstie"
__email__ = "simen.roko.krogstie@nmbu.no"
"""

lisp = '''
(defun LaTeX-newline ()
  "Start a new line potentially staying within comments.
This depends on `LaTeX-insert-into-comments'."
  (interactive)
  (if LaTeX-insert-into-comments
      (cond ((and (save-excursion (skip-chars-backward " \t") (bolp))
                  (save-excursion
                    (skip-chars-forward " \t")
                    (looking-at (concat TeX-comment-start-regexp "+"))))
             (beginning-of-line)
             (insert (buffer-substring-no-properties
                      (line-beginning-position) (match-end 0)))
             (newline))
            ((and (not (bolp))
                  (save-excursion
                    (skip-chars-forward " \t") (not (TeX-escaped-p)))
                  (looking-at
                   (concat "[ \t]*" TeX-comment-start-regexp "+[ \t]*")))
             (delete-region (match-beginning 0) (match-end 0))
             (indent-new-comment-line))
            ;; `indent-new-comment-line' does nothing when
            ;; `comment-auto-fill-only-comments' is non-nil, so we
            ;; must be sure to be in a comment before calling it.  In
            ;; any other case `newline' is used.
            ((TeX-in-comment)
             (indent-new-comment-line))
            (t
             (newline)))
    (newline)))
'''


def check_parentheses(text):
    max_depth = 0; is_valid = True ;is_balanced = True
    sjekk = []
    sum_= 0
    
    for lines in range(0, len(text)):
        for words in range(0, len(text[lines])):
            if text[lines][words] == '(' :
                    sjekk.append(1)
            elif text[lines][words] == ')':
                    sjekk.append(-1)
        
    for idx in range(0, len(sjekk)):
        if sjekk[idx] == 1:
            sum_ += 1
        else:
            sum_ -= 1
        if sum_ < 0:
            is_valid = False
        if sum_ > max_depth:
            max_depth = sum_ 
    if sum_ != 0:
            is_balanced = False
        
    return ((max_depth, is_valid, is_balanced))

res = check_parentheses(lisp)
print('max_dept:', res[0], 'valid:', res[1], 'balanced:', res[2])

#%%
"""
max_depth = 8
is_valid = True
is_balanced = True
"""






