# -*- coding: utf-8 -*-
"""
Created on Thu Feb  8 14:27:00 2024

@author: TG
"""


f = open('matriz_transp_guardado.txt', 'w')


nrbits=4
#para testar (tempo dado para cada operação de multiplicação [ns])
tempo=2
tempo_total=(2**nrbits)*(((2**nrbits)+1)*tempo)
f.write("\n--testar durante "+str(tempo_total)+" ps \n\n")


lines1 = ['library IEEE;',
         'use IEEE.std_logic_1164.all;',
         'use IEEE.std_logic_arith.all;',
         ' ',
         '-- Uncomment the following library declaration if using',
         '-- arithmetic functions with Signed or Unsigned values',
         '--use IEEE.NUMERIC_STD.ALL;',
         ' ',
         '-- Uncomment the following library declaration if instantiating',
         '-- any Xilinx primitives in this code.',
         '--library UNISIM;',
         '--use UNISIM.VComponents.all;',
         ' ',
         ' ',
         'entity semi_somador is',
         '	port (',
         '		A : in std_logic;',
         '		B : in std_logic;',
         ' ',
         '		S : out std_logic;',
         '		Carry_Out : out std_logic',
         '	);',
         'end semi_somador;',
         ' ',
         'architecture structure of semi_somador is',
         'begin',
         '	S <=  A xor B;',
         '	Carry_Out <= A and B;',
         'end structure;',
         ' ',
         '----------------------------------------------------------------',
         'library IEEE;',
         'use IEEE.std_logic_1164.all;',
         'use IEEE.std_logic_arith.all;',
         ' ',
         'entity somador is',
         '	port (',
         '		A : in std_logic;',
         '		B : in std_logic;',
         '		Carry_In : in std_logic;',
         ' ',
         '		S : out std_logic;',
         '		Carry_Out : out std_logic',
         '	);',
         'end somador;',
         ' ',
         'architecture structure of somador is',
         ' ',
         'begin',
         '	S <= (A xor B) xor Carry_In;',
         '	Carry_Out  <= (A and B) or (A and Carry_In) or (B and Carry_In);',
         'end structure;',
         ' ',
         '----------------------------------------------------------------',
         ' ',
         'library IEEE;',
         'use IEEE.std_logic_1164.all;',
         'use IEEE.std_logic_arith.all;',
         ' ',
         'entity multiplicador_matriz_transp_guardado is',
         '	port (',
         "		X : in std_logic_vector ("+str((nrbits-1))+" downto 0);",
         "		Y : in std_logic_vector ("+str((nrbits-1))+" downto 0);",
         "		P : out std_logic_vector ("+str((2*nrbits-1))+" downto 0)",
         '	);',
         'end multiplicador_matriz_transp_guardado;',
         ' ',
         'architecture structure of multiplicador_matriz_transp_guardado is',
         ' ',
         'component semi_somador',
         '	port (',
         '		A : in std_logic;',
         '		B : in std_logic;',
         ' ',
         '		S : out std_logic;',
         '		Carry_Out : out std_logic',
         '	);',
         'end component;',
         ' ',
         'component somador',
         '	port (',
         '		A : in std_logic;',
         '		B : in std_logic;',
         '		Carry_In : in std_logic;',
         ' ',
         '		S : out std_logic;',
         '		Carry_Out : out std_logic',
         '	);',
         'end component;',
         ' ']


lines2=[' ']

lines2.append('--produtos parciais')
for i in range(0,(nrbits)):
    lines2.append("signal and"+str(i)+" : std_logic_vector ("+str((nrbits-1))+" downto 0);")
lines2.append(' ')


lines2.append("signal transp1_1 : std_logic;")
for i in range(2,(nrbits)):
    lines2.append("signal transp"+str(i)+" : std_logic_vector ("+str(i)+" downto 1);")
for i in range(nrbits,(2*nrbits-2)):
    lines2.append("signal transp"+str(i)+" : std_logic_vector ("+str((2*nrbits-1)-i)+" downto 1);")
lines2.append(' ')

for i in range(2,(nrbits)):
    lines2.append("signal soma"+str(i)+" : std_logic_vector ("+str(i)+" downto 1);")
for i in range(nrbits,(2*nrbits-2)):
    lines2.append("signal soma"+str(i)+" : std_logic_vector ("+str((2*nrbits-1)-i)+" downto 1);")
lines2.append(' ')

lines2.append('begin')

for i in range(0,(nrbits)):
    for j in range(0,(nrbits)):
        lines2.append("	and"+str(i)+"("+str(j)+") <= X("+str(i)+") and Y("+str(j)+");")
lines2.append(' ')

	#i->coluna
	#j->linha
	
	#i=0
        
lines2.append('	--P(0)')
lines2.append("	P(0) <= and"+str(0)+"("+str(0)+");")
lines2.append(' ')

if nrbits>1:
    for  i in range(1, (2*nrbits-1)):
        if i==1:
            j=1
            x=0
            y=i
            lines2.append('	--P(1)')
            lines2.append("	coluna"+str(i)+"_"+str(j)+": semi_somador port map (A => and"+str(1)+"("+str(0)+"), B  => and"+str(0)+"("+str(1)+"), S => P(1), Carry_Out => transp1_1);")
            #colunai_j: semi_somador port map (A => (X(1) and Y(0)), B  => (X(0) and Y(1)), S => P(1), Carry_Out => transpi(j);
        if (i>1)and (i<(nrbits)):
            #2<=nr coluna<nrbits
            #nrlinha=1
            j=1
            x=0
            y=i
            lines2.append("	coluna"+str(i)+"_"+str(j)+": somador port map (A => and"+str(x)+"("+str(y)+"), B  => and"+str(x+1)+"("+str(y-1)+"), Carry_In => and"+str(x+2)+"("+str(y-2)+"), S => soma"+str(i)+"("+str(j)+"), Carry_Out => transp"+str(i)+"("+str(j)+"));")
            #colunai_j: somador port map (A => (X(x) and Y(y)), B  => (X(x+1) and Y(y-1)), Carry_In => (X(x+2) and Y(y-2)), S => somai(j), Carry_Out => transpi(j));           
            #2<=nrlinha<nrcoluna
            x=3
            y=i-3
            for j in range (2, i):
                lines2.append("	coluna"+str(i)+"_"+str(j)+": somador port map (A => soma"+str(i)+"("+str(j-1)+"), B  => and"+str(x)+"("+str(y)+"), Carry_In => transp"+str(i-1)+"("+str(j-1)+"), S => soma"+str(i)+"("+str(j)+"), Carry_Out => transp"+str(i)+"("+str(j)+"));")
                #colunai_j: somador port map (A => somai(j-1), B  => (X(x) and Y(y)), Carry_In => transpi-1(j-1), S => somai(j), Carry_Out => transpi(j));
                x=x+1
                y=y-1
            #nrlinha=nrcoluna (semi-somador)
            j=j+1
            if i==2:
                lines2.append("	coluna"+str(i)+"_"+str(j)+": semi_somador port map (A => soma"+str(i)+"("+str(j-1)+"), B  => transp1_1, S => P("+str(i)+"), Carry_Out => transp"+str(i)+"("+str(j)+"));")
            else:
                lines2.append("	coluna"+str(i)+"_"+str(j)+": semi_somador port map (A => soma"+str(i)+"("+str(j-1)+"), B  => transp"+str(i-1)+"("+str(j-1)+"), S => P("+str(i)+"), Carry_Out => transp"+str(i)+"("+str(j)+"));")
            #colunai_j: semi_somador port map (A => somai(j-1), B  => transpi-1(j-1), S => P(i), Carry_Out => transpi(j));
        if i==nrbits:
            #nr coluna=nrbits
            #nrlinha=1
            j=1
            x=1
            y=i-1
            lines2.append("	coluna"+str(i)+"_"+str(j)+": somador port map (A => and"+str(x)+"("+str(y)+"), B  => and"+str(x+1)+"("+str(y-1)+"), Carry_In => transp"+str(i-1)+"("+str(j)+"), S => soma"+str(i)+"("+str(j)+"), Carry_Out => transp"+str(i)+"("+str(j)+"));")
            #colunai_j: somador port map (A => (X(x) and Y(y)), B  => (X(x+1) and Y(y-1)), Carry_In => transpi-1(j), S => somai(j), Carry_Out => transpi(j);
            #2<=nrlinha<nrcoluna
            x=3
            y=i-3
            for j in range (2, i-1):
                lines2.append("	coluna"+str(i)+"_"+str(j)+": somador port map (A => soma"+str(i)+"("+str(j-1)+"), B  => and"+str(x)+"("+str(y)+"), Carry_In => transp"+str(i-1)+"("+str(j)+"), S => soma"+str(i)+"("+str(j)+"), Carry_Out => transp"+str(i)+"("+str(j)+"));")
                #colunai_j: somador port map (A => somai(j-1), B  => (X(x) and Y(y)), Carry_In => transpi-1(j), S => somai(j), Carry_Out => transpi(j));
                x=x+1
                y=y-1
            #nrlinha=nrcoluna (semi-somador)
            j=j+1
            lines2.append("	coluna"+str(i)+"_"+str(j)+": semi_somador port map (A => soma"+str(i)+"("+str(j-1)+"), B  => transp"+str(i-1)+"("+str(j)+"), S => P("+str(i)+"), Carry_Out => transp"+str(i)+"("+str(j)+"));")
            #colunai_j: semi_somador port map (A => somai(j-1), B  => transpi-1(j), S => P(i), Carry_Out => transpi(j));
        if (i>nrbits)and (i<nrbits*2-2):
            #nrbits+1<=nr coluna<((2*nrbits)-2)
            #nrlinha=1
            j=1
            x=i-(nrbits-1)
            y=nrbits-1
            lines2.append("	coluna"+str(i)+"_"+str(j)+": somador port map (A => and"+str(x)+"("+str(y)+"), B  => and"+str(x+1)+"("+str(y-1)+"), Carry_In => transp"+str(i-1)+"("+str(j)+"), S => soma"+str(i)+"("+str(j)+"), Carry_Out => transp"+str(i)+"("+str(j)+"));")
            #colunai_j: somador port map (A => (X(x) and Y(y)), B  => (X(x+1) and Y(y-1)), Carry_In => transpi-1(j), S => somai(j), Carry_Out => transpi(j));
            #2<=nrlinha<((2*nrbits)-1)-nrcoluna
            for j in range (2, ((2*nrbits)-1)-i):
                lines2.append("	coluna"+str(i)+"_"+str(j)+": somador port map (A => soma"+str(i)+"("+str(j-1)+"), B  => and"+str(x)+"("+str(y)+"), Carry_In => transp"+str(i-1)+"("+str(j)+"), S => soma"+str(i)+"("+str(j)+"), Carry_Out => transp"+str(i)+"("+str(j)+"));")
                #colunai_j: somador port map (A => somai(j-1), B  => (X(x) and Y(y)), Carry_In => transpi-1(j), S => somai(j), Carry_Out => transpi(j));
                x=x+1
                y=y-1
            #nrlinha=((2*nrbits)-1)-nrcoluna
            j=j+1
            lines2.append("	coluna"+str(i)+"_"+str(j)+": somador port map (A => soma"+str(i)+"("+str(j-1)+"), B  => transp"+str(i-1)+"("+str(j)+"), Carry_In => transp"+str(i-1)+"("+str(j+1)+"), S => P("+str(i)+"), Carry_Out => transp"+str(i)+"("+str(j)+"));")
            #colunai_j: somador port map (A => somai(j-1), B  => transpi-1(j), Carry_In => transpi-1(j+1), S => P(i), Carry_Out => transpi(j));
        if i==nrbits*2-2:
            #nr coluna=((2*nrbits)-2)
            j=1
            x=y=nrbits-1            
            lines2.append("	coluna"+str(i)+"_"+str(j)+": somador port map (A => and"+str(x)+"("+str(y)+"), B  => transp"+str(i-1)+"("+str(j)+"), Carry_In => transp"+str(i-1)+"("+str(j+1)+"), S => P("+str(i)+"), Carry_Out => P("+str(i+1)+"));")
            #colunai_j: somador port map (A => (X(x) and Y(y)), B  => transpi-1(j), Carry_In => transpi-1(j+1), S => P(i), Carry_Out => P(i+1));
        lines2.append(' ')

lines2.append('end structure;')
lines2.append(' ')
lines2.append('-------------------------------------------------')
lines2.append(' ')
lines2.append('library IEEE;')
lines2.append('use IEEE.std_logic_1164.all;')
lines2.append('use IEEE.std_logic_arith.all;')
lines2.append(' ')
lines2.append('entity test_bench_multiplicador_matriz_transp_guardado is')
lines2.append('end test_bench_multiplicador_matriz_transp_guardado;')
lines2.append(' ')
lines2.append('architecture Behavioral of test_bench_multiplicador_matriz_transp_guardado is')
lines2.append(' ')
lines2.append('	component multiplicador_matriz_transp_guardado')
lines2.append('		port (')
lines2.append("			X : in std_logic_vector ("+str((nrbits-1))+" downto 0);")
lines2.append("			Y : in std_logic_vector ("+str((nrbits-1))+" downto 0);")
lines2.append("			P : out std_logic_vector ("+str((2*nrbits-1))+" downto 0)")                     
lines2.append('		);')
lines2.append('	end component;')
lines2.append(' ')
lines2.append("	signal X, Y : std_logic_vector ("+str((nrbits-1))+" downto 0);")
lines2.append("	signal P : std_logic_vector ("+str((2*nrbits-1))+" downto 0);")
lines2.append('	signal reset : std_logic;')
lines2.append(' ')
lines2.append('begin')
lines2.append(' ')
lines2.append('	mult : multiplicador_matriz_transp_guardado port map (X, Y, P);')
lines2.append(' ')
lines2.append('	increment_X : process')
lines2.append('	begin')
lines2.append("		if reset='1' then")
lines2.append(' ')


lines3=['			X <= "']
for i in range(0,(nrbits)):
    lines3.append('0')
lines3.append('";')

lines4=[' ']
lines4.append('		else')
lines4.append('			X <= unsigned(X)+1;')
lines4.append('		end if;')
lines4.append('		--tempo X=(2**nrbits)*tempo Y')
lines4.append("		wait for "+str((2**nrbits)*tempo)+" ps ;")
lines4.append('	end process increment_X;')
lines4.append(' ')

lines4.append('	increment_Y : process')
lines4.append('	begin')
lines4.append("		if reset='1' then")
lines4.append(' ')


lines5=['			Y <= "']
for i in range(0,(nrbits)):
    lines5.append('0')
lines5.append('";')

lines6=[' ']
lines6.append('		else')
lines6.append('			Y <= unsigned(Y)+1;')
lines6.append('		end if;')
lines6.append("		wait for "+str(tempo)+" ps ;")
lines6.append('	end process increment_Y;')
lines6.append(' ')
lines6.append('	init : process')
lines6.append('	begin')
lines6.append("		reset <= '1', '0' after "+str((2**nrbits+1)*tempo)+" ps ;")
lines6.append('		wait;')
lines6.append('	end  process init;')
lines6.append(' ')
lines6.append('end Behavioral;')
lines6.append('')
lines6.append('')
lines6.append('')
lines6.append('')
lines6.append('')
lines6.append('')
lines6.append('')
lines6.append('')



f.write('\n'.join(lines1))
f.write('\n'.join(lines2))
f.write(''.join(lines3))
f.write('\n'.join(lines4))
f.write(''.join(lines5))
f.write('\n'.join(lines6))

f.close()
