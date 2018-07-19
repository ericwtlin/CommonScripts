"syntax enable
syntax on
set nu

"支持鼠标选项
set mouse=a  

"编辑时一个TAB字符占多少个空格的位置。
set tabstop=4

"shiftwidth是默认缩进宽度,例如 “:10,20>”表示把10到20行缩进1次，这时就是shiftwidth控制宽度
set shiftwidth=4

"开启时，在行首按TAB将加入shiftwidth个空格，否则加入tabstop个空格。
set smarttab

"自动设置当前文件目录为工作目录
set autochdir

"自动缩进或C风格缩进
"set autoindent
"set cindent

"智能缩进:每一行都和前一行有相同的缩进量,
"同时这种缩进形式能正确的识别出花括号,当遇到右花括号（}）,
"则取消缩进形式。此外还增加了识别C语言关键字的功能。
"如果一行是以#开头的(比如宏)，那么这种格式将会被特殊对待而不采用缩进格式
set smartindent


"用space替代tab的输入
set expandtab	 
"每次退格将删除4个空格，对应开启expendtab
set softtabstop=4


"设置初始窗口大小
"set lines=40
"set columns=110


"设置软换行
set wrap
set linebreak


"设置文件的代码形式
set encoding=utf-8
set termencoding=utf-8
set fileencoding=utf-8
set fileencodings=ucs-bom,utf-8,chinese,cp936

"vim的菜单乱码解决：
source $VIMRUNTIME/delmenu.vim
source $VIMRUNTIME/menu.vim
  
"vim提示信息乱码的解决
language messages zh_CN.utf-8

set t_Co=256


"设定配色方案
colorscheme desert

"解决ubuntu下字体间距过大的问题
if has("gui_gtk2")
set guifont=DejaVu\ Sans\ Mono\ 11
elseif has("gui_macvim")
set guifont=DejaVu_Sans_Mono:h11
elseif has("gui_win32")
set guifont=DejaVu_Sans_Mono:h11
end

set nocompatible
source $VIMRUNTIME/vimrc_example.vim
source $VIMRUNTIME/mswin.vim
behave mswin





""""""""""""""""""""""""""""""""""""""""""""""
"  Taglist
""""""""""""""""""""""""""""""""""""""""""""""

"nmap <C-F5> <Esc>:!ctags -R *<CR>         "
"使用ctrl+<F5>键运行Ctags,(下面自动补全的omnicppcomplete也用到ctags，此处注释掉)
let Tlist_Auto_Open = 0                 " 启动vim不自动打开taglist窗口
let Tlist_Use_Right_Window = 1          " 设置taglist窗口出现在右侧
let Tlist_File_Fold_Auto_Close = 1      " taglist只显示当前文件tag，其它文件的tag都被折叠起来
let Tlist_Exit_OnlyWindow = 1           " 如果taglist窗口是最后一个窗口退出vim
let Tlist_Sort_Type = "name"            " 设置taglist以tag名字进行排序
let Tlist_Use_SingleClick = 1           " 单击tag就跳转
let Tlist_Process_File_Always = 1       " 设置taglist始终解析文件中的tag，不管taglist窗口有没有打开
map <silent> <F7> :TlistToggle<cr>      " 使用<F7>键就打开/关闭taglist窗口
if has("gui_running")
    let Tlist_Inc_Winwidth = 0
else
    let Tlist_Inc_Winwidth = 1
endif



""""""""""""""""""""""""""""""""""""""""""""""
" NERDTree
""""""""""""""""""""""""""""""""""""""""""""""
map <silent> <F6> :NERDTreeToggle<cr> " 使用<F6>键就打开/关闭NERDTree窗口
let NERDTreeMinimalUI = 1 " 关闭书签标签('Press ? for help')
let NERDTreeDirArrows = 1 " 改变目录结点的显示方式(+/~)
"autocmd VimEnter * NERDTree "默认打开



""""""""""""""""""""""""""""""""""""""""""""""
" minibufexpl.vim
""""""""""""""""""""""""""""""""""""""""""""""

" ctrl+tab shift+ctrl+tab 切换缓冲区里的文件
let g:miniBufExplMapWindowNavVim = 1 
let g:miniBufExplMapWindowNavArrows = 1 
let g:miniBufExplMapCTabSwitchBufs = 1 
let g:miniBufExplModSelTarget = 1 





""""""""""""""""""""""""""""""""""""""""""""""
" OmniCppComplete配置
""""""""""""""""""""""""""""""""""""""""""""""
set nocp
filetype plugin on
map <C-F5> :!ctags -R --c++-kinds=+p --fields=+iaS --extra=+q .<CR>   "使用Ctrl+F5键生成OmniCppComplete使用的tag文件
set completeopt=menu
set cindent

:inoremap ( ()<ESC>i
:inoremap ) <c-r>=ClosePair(')')<CR>
:inoremap { {}<ESC>i
:inoremap } <c-r>=ClosePair('}')<CR>
:inoremap [ []<ESC>i
:inoremap ] <c-r>=ClosePair(']')<CR>
":inoremap < <><ESC>i
":inoremap > <c-r>=ClosePair('>')<CR>
"':inoremap " ""<ESC>i
":inoremap ' ''<ESC>i

function ClosePair(char)
if getline('.')[col('.') - 1] == a:char
return "\<Right>"
else
return a:char
endif
endf


let OmniCpp_GlobalScopeSearch = 1 " 0 or 1
let OmniCpp_NamespaceSearch = 1 " 0 , 1 or 2
let OmniCpp_DisplayMode = 1
let OmniCpp_ShowScopeInAbbr = 0
let OmniCpp_ShowPrototypeInAbbr = 1
let OmniCpp_ShowAccess = 1
let OmniCpp_MayCompleteDot = 1
let OmniCpp_MayCompleteArrow = 1
let OmniCpp_MayCompleteScope = 1

set tags+=~/.vim/tags/systags
set tags+=tags


"winmanager
"let g:winManagerWindowLayout="NERDTree|TagList"
"let g:winManagerWindowLayout="TagList|FileExplorer,BufExplorer"
"let g:NERDTree_title="[NERDTree123]"
"nmap <C-m> :WMToggle<CR>

"function! NERDTree_Start()  
"    exec 'NERDTree'  
"endfunction

"function! NERDTree_IsValid()  
"    return 1  
"endfunction

"let g:AutoOpenWinManager = 1

"if g:AutoOpenWinManager
"	autocmd VimEnter * nested call s:ToggleWindowsManager()d w 
"endif
