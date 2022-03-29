" vim:fdm=marker


" Mouse and clipboard {{{
set mouse=a                           " Enable mouse in all modes
set ttymouse=xterm2
set clipboard=unnamedplus             " Use system clipboard by default
" }}}

" Visual improvements {{{
syntax on
set number                            " Show line numbers
set cursorline                        " Highlight line where the cursor is
set wildmenu                          " Improved command line completion
set laststatus=2                      " Always shows status bar
highlight OverLength ctermbg=red ctermfg=lightgray guibg=#6D0000
match OverLength /\%81v/
set listchars=tab:➟\ ,eol:⤦           " Cool characters when use set list
set term=xterm-256color-italic
if has("termguicolors")
  set termguicolors
endif
" }}}

" Ctags {{{
  " Need to run `ctags -R --tag-relative=yes -f ./.git/tags WCN/lib/`
  " periodically.
  " (Create a .git/hooks/post-checkout with that command for example)
set tags=~/dev/vX/.git/tags
" }}}

" Tab and spaces {{{
set tabstop=2
set expandtab
set smartindent
set shiftwidth=2
set softtabstop=2
set switchbuf=usetab
" }}}

" Search {{{
set hlsearch                          " Highlight search
set incsearch                         " Incremental search
nmap <silent> ,/ :nohlsearch<CR>      " Use ,/ to clear search
nnoremap <C-]> g<C-]>
" }}}

" File enconding {{{
"set bomb                             " Don't really like bomb :-/
set fileencoding=utf-8                " UTF8!!
" }}}

" NO backups {{{
" Use git instead :)
" set nobackup
set nowritebackup
" }}}

" Persistent undo files {{{
if has('persistent_undo')
  let s:undodir = $HOME . "/.vim/undo"
  if exists("*mkdir")
    try
      call mkdir(s:undodir)
    catch
    endtry
  endif
  execute "set undodir=" . s:undodir
  set undofile
endif
" }}}

set nocompatible

" Window navigation {{{
" This mappings allow me to use ctrl+h/j/k/l to move between windows
nnoremap <C-h> <esc><C-w>h
nnoremap <C-j> <esc><C-w>j
nnoremap <C-k> <esc><C-w>k
nnoremap <C-l> <esc><C-w>l
inoremap <C-h> <esc><C-w>h
inoremap <C-j> <esc><C-w>j
inoremap <C-k> <esc><C-w>k
inoremap <C-l> <esc><C-w>l
inoremap <esc><C-h> <C-w>h
inoremap <esc><C-j> <C-w>j
inoremap <esc><C-k> <C-w>k
inoremap <esc><C-l> <C-w>l

" Close quickfix with double escape
nnoremap <esc><esc> :ccl<CR>
" }}}

" Tabs, alt mappings {{{
" This mappings allow me to change tab by alt+l/h and alt+number
nnoremap <esc>l <esc>gt<CR>
nnoremap <esc>h <esc>gT<CR>
nnoremap <esc>n <esc>:tabnew<CR>
nnoremap <esc>1 <esc>1gt
nnoremap <esc>2 <esc>2gt
nnoremap <esc>3 <esc>3gt
nnoremap <esc>4 <esc>4gt
nnoremap <esc>5 <esc>5gt
nnoremap <esc>6 <esc>6gt
nnoremap <esc>7 <esc>7gt
nnoremap <esc>8 <esc>8gt
nnoremap <esc>9 <esc>9gt
" }}}

" Tab navigation {{{
" Allows me to go to last selected tab by pressing altgr+t
let g:lasttab = 1
augroup tabs
  autocmd!
  autocmd TabLeave * let g:lasttab = tabpagenr()
augroup END
nnoremap ŧ :exe "tabn ".g:lasttab<CR>
" }}}

" Tidy/format Files {{{
"
"   Description:
"     * Sets formatprg so you can tidy up your code using gq.
"     * Maps F8 to gq.
"
"   Setup:
"     You need in your system the formatting tool you want to use
"     (obviously!).
"
"     Some tools you might want to use:
"     ----------------------------------------------------------------
"      filetype | visual_mode | tool       | install cmd 
"     ----------------------------------------------------------------
"      json     | no          | fixjson    | npm install -g fixjson
"      perl     | yes         | perltidy   | apt install perltidy
"      python   | no          | autopep8   | apt install python3-autopep8
"      python   | no          | yapf3      | apt install yapf3
"      xml      | yes         | xmllint    | apt install libxml2-utils
"     ----------------------------------------------------------------
" 
"     Some tools only work for the full file. With others you can
"     go to visual mode and select a chunk of the file.
"
"   Alternatives:
"     Vim ALE has the command :ALEFix that works in a similar way.
"

" Tidy entire buffer and return cursor to original position
function! OleeoTidyFile()
    let l = line(".")
    let c = col(".")
    execute("normal! ggVGgq")
    call cursor(l, c)
endfun

" Set tools for tyding up files
augroup oleeo_format
  autocmd!
  autocmd Filetype perl setlocal formatprg=perltidy
  "autocmd FileType python setlocal formatprg=autopep8\ -aa\ --indent-size\ 4\ -
  autocmd FileType python setlocal formatprg=yapf3
  autocmd FileType xml setlocal formatprg=xmllint\ --format
  autocmd FileType json setlocal formatprg=fixjson
augroup END

" Mappings I like
nnoremap <F8> :call OleeoTidyFile()<CR>
vnoremap <F8> gq
" }}}

" Keymaps of F keys {{{
nnoremap ! :!
nnoremap <F2> :set paste!<CR>
nnoremap <F9> :Gstatus<CR>
nnoremap <F10> :Gdiff<CR>
nnoremap <F12> :Tagbar<CR>
" }}}

" No more Ex mode: http://www.bestofvim.com/tip/leave-ex-mode-good/
nnoremap Q <nop>

" Install Plugin Manager {{{
if empty(glob('~/.vim/autoload/plug.vim'))
  silent !curl -fLo ~/.vim/autoload/plug.vim --create-dirs
    \ https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim
  autocmd VimEnter * PlugInstall --sync | source $MYVIMRC
endif
" }}}


" Install Plugins {{{
call plug#begin('~/.vim/plugged')

" ### Utitilies to open files easily ###
    " Plug 'ctrlpvim/ctrlp.vim'
    " Plug 'DavidEGx/ctrlp-smarttabs'
Plug 'junegunn/fzf'
Plug 'junegunn/fzf.vim'

" Fancy start scren for vim
Plug 'mhinz/vim-startify'

" ### Visual improvements ###
" Show marks on the side
Plug 'kshenoy/vim-signature'
" Cool status bar
Plug 'vim-airline/vim-airline'
Plug 'vim-airline/vim-airline-themes'
let g:airline#extensions#tabline#fnamemod = ':t'
" Allows to highlight words
" Plug 'DavidEGx/VimMarkForVundle'
" Colorschemes
Plug 'morhetz/gruvbox'
" Automatically highlight variables whenever the cursor is there
Plug 'azabiong/vim-highlighter'
" Plug 'DavidEGx/vim-variable-highlighting'

" ### Version Control improvements ###
Plug 'tpope/vim-fugitive'

  " Git functions for vim
  " Only using vim-fugitive nowadays
  " Plugin 'git://repo.or.cz/vcscommand'

" Shows modifications of files on the side
Plug 'airblade/vim-gitgutter'

" ### Other functionalities ###
" Show function list
Plug 'majutsushi/tagbar'
" Syntax checker
Plug 'dense-analysis/ale'

" Allow to use * with selected text in visual mode
Plug 'thinca/vim-visualstar'

call plug#end()
" filetype plugin indent on
" }}}

" Plugin configurations {{{
let g:startify_disable_at_vimenter = 0
let g:startify_bookmarks     = [ '~/.vimrc', '~/.tmux.conf' ]
let g:startify_files_number  = 15
let g:startify_change_to_dir = 0
let g:startify_relative_path = 1
autocmd User Startified setlocal buftype=

let g:gitgutter_sign_modified='≠'

let g:airline#extensions#tabline#enabled = 1
let g:airline#extensions#tagbar#enabled = 1
let g:airline#extensions#hunks#enabled=0
" let g:airline_left_sep = '▶'
" let g:airline_right_sep = '◀'
" let g:airline#extensions#tabline#left_sep = '▷'
" let g:airline#extensions#tabline#left_alt_sep = '▷'
let g:airline_theme='deus'

let g:ale_fixers = {
\   '*': ['remove_trailing_lines', 'trim_whitespace'],
\   'javascript': ['eslint'],
\   'perl': { 'command': 'perltidy -b' },
\   'xml': ['xmllint'],
\   'python': ['autopep8']
\}

let g:airline#extensions#ale#enabled = 1

" let g:ctrlp_match_window = 'bottom,order:ttb,min:10,max:20,results:20'
" let g:ctrlp_working_path_mode = '0'
" let g:ctrlp_extensions = ['smarttabs']
" let g:ctrlp_smarttabs_reverse = 0
" let g:ctrlp_smarttabs_modify_tabline = 1
" let g:ctrlp_smarttabs_exclude_quickfix = 1
" let g:ctrlp_clear_cache_on_exit = 1

nnoremap <C-p> :Files<CR>
inoremap <C-p> <ESC>:Files<CR>
nnoremap þ :Windows<CR>
inoremap þ <ESC>:Windows<CR>
set grepprg=ag\ --nogroup\ --nocolor\ -p\ /home/david/.agignore
" nnoremap <Leader>k :grep! "\b<C-R><C-W>\b"<CR>:botright cwindow<CR>
nnoremap <Leader>k :Ag! <C-R><C-W><CR>
vnoremap <Leader>k :<C-U>execute('grep! "\b' . g:Get_visual_selection() . '\b"\|botright cwindow')<CR><CR>
command! -bang -nargs=? -complete=dir Files
  \ call fzf#vim#files(<q-args>, fzf#vim#with_preview(), <bang>0)

" {{{
" Command for git grep
" - fzf#vim#grep(command, with_column, [options], [fullscreen])
command! -bang -nargs=* GGrep
  \ call fzf#vim#grep(
  \   'git grep --line-number '.shellescape(<q-args>), 0,
  \   { 'dir': systemlist('git rev-parse --show-toplevel')[0] }, <bang>0)

" Override Colors command. You can safely do this in your .vimrc as fzf.vim
" will not override existing commands.
command! -bang Colors
  \ call fzf#vim#colors({'left': '15%', 'options': '--reverse --margin 30%,0'}, <bang>0)

" Augmenting Ag command using fzf#vim#with_preview function
"   * fzf#vim#with_preview([[options], [preview window], [toggle keys...]])
"     * For syntax-highlighting, Ruby and any of the following tools are required:
"       - Bat: https://github.com/sharkdp/bat
"       - Highlight: http://www.andre-simon.de/doku/highlight/en/highlight.php
"       - CodeRay: http://coderay.rubychan.de/
"       - Rouge: https://github.com/jneen/rouge
"
"   :Ag  - Start fzf with hidden preview window that can be enabled with "?" key
"   :Ag! - Start fzf in fullscreen and display the preview window above
command! -bang -nargs=* Ag
  \ call fzf#vim#ag(<q-args>,
  \                 <bang>0 ? fzf#vim#with_preview('right:50%')
  \                         : fzf#vim#with_preview('right:50%:hidden', '?'),
  \                 <bang>0)

" Similarly, we can apply it to fzf#vim#grep. To use ripgrep instead of ag:
command! -bang -nargs=* Ag
  \ call fzf#vim#grep(
  \   'rg --column --line-number --no-heading --color=always --smart-case '.shellescape(<q-args>), 1,
  \   <bang>0 ? fzf#vim#with_preview('up:60%')
  \           : fzf#vim#with_preview('right:50%:hidden', '?'),
  \   <bang>0)

" Likewise, Files command with preview window
command! -bang -nargs=? -complete=dir Files
  \ call fzf#vim#files(<q-args>, fzf#vim#with_preview(), <bang>0)
" }}}

" The Silver Searcher
" if executable('ag')
"   " Use ag over grep
"   set grepprg=ag\ --nogroup\ --nocolor\ -p\ /home/david/.agignore
"
"   " Use ag in CtrlP for listing files. Lightning fast and respects .gitignore
"   let g:ctrlp_user_command = 'ag %s -l --nocolor -p /home/david/.agignore -g ""'
"
"   " ag is fast enough that CtrlP doesn't need to cache
"   let g:ctrlp_use_caching = 0
"
"   " bind K to grep word under cursor
"   nnoremap <Leader>k :grep! "\b<C-R><C-W>\b"<CR>:botright cwindow<CR>
"   vnoremap <Leader>k :<C-U>execute('grep! "\b' . g:Get_visual_selection() . '\b"\|botright cwindow')<CR><CR>
"
"   command! -nargs=+ -complete=file -bar Ag silent! grep! <args>|botright cwindow|redraw!
" endif

function! g:Get_visual_selection()
  " Why is this not a built-in Vim script function?!
  let [lnum1, col1] = getpos("'<")[1:2]
  let [lnum2, col2] = getpos("'>")[1:2]
  let lines = getline(lnum1, lnum2)
  let lines[-1] = lines[-1][: col2 - (&selection == 'inclusive' ? 1 : 2)]
  let lines[0] = lines[0][col1 - 1:]
  return join(lines, "\n")
endfunction

let g:qfenter_keymap = {}
let g:qfenter_keymap.vopen = ['<C-v>']
let g:qfenter_keymap.hopen = ['<C-CR>', '<C-s>', '<C-x>']
let g:qfenter_keymap.topen = ['<C-t>']

" }}}

" Color scheme {{{
let colors = globpath(&runtimepath, printf('colors/%s.vim', 'gruvbox'), 1, 1)
if (len(colors) > 0)
  let g:gruvbox_italic = 1
  if !has("gui_running")
    let g:gruvbox_italic = 0
  endif
  set background=dark | colorscheme gruvbox
endif

" Other good colorschemes:
" set t_Co=256 | colorscheme xoria256
" set t_Co=256  | colorscheme molokai
" }}}


