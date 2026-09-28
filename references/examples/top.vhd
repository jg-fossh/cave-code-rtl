--------------------------------------------------------------------------------
-- Company:      AI Electronics Design Inc.
-- Engineer:     Hardware Engineer
-- Create Date:  2026
-- Design Name:  Generic N-bit Synchronous Up-Counter
-- Module Name:  counter - Behavioral
-- Description:  A comprehensive VHDL example demonstrating generics, ports,
--               sequential processes, and standard numeric packages.
--------------------------------------------------------------------------------

-- Section 1: Libraries and Packages
-- Crucial for defining standard logic types and arithmetic operations.
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL; -- Preferred over std_logic_arith for synthesis

-- Section 2: Entity Declaration
-- Defines the interface (Inputs, Outputs, and Parameters) of the module.
entity counter is
    generic (
        BIT_WIDTH : positive := 8; -- Allows the module to be resized easily
        BIT_NUM   : natural  := 8
    );
    port (
        clk    : in  std_logic;                               -- System Clock
        reset  : in  std_logic;                               -- Active High Synchronous Reset
        enable : in  std_logic;                               -- Count Enable signal
        count  : out std_logic_vector(BIT_WIDTH-1 downto 0)   -- Current Counter Value
    );
end entity counter;

-- Section 3: Architecture Body
-- Describes the internal behavior or structure of the design.
architecture Behavioral of counter is

    -- Internal signal to hold the counter state (unsigned for math ops)
    signal r_count : unsigned(BIT_WIDTH-1 downto 0) := (others => '0');

begin

    -- Sequential Process: Executed every time a signal in the sensitivity list changes.
    -- For synchronous logic, we only look at the clock signal.
    p_counter_seq : process(clk)
    begin
        if rising_edge(clk) then
            if reset = '1' then
                -- Synchronous Reset: Resets internal register to all zeros
                r_count <= (others => '0');
            elsif enable = '1' then
                -- Increments internal register when enabled
                r_count <= r_count + 1;
            end if;
        end if;
    end process p_counter_seq;

    -- Concurrent Assignment: Continuously maps internal unsigned register to outer port.
    -- Type casting is required from 'unsigned' to 'std_logic_vector'.
    count <= std_logic_vector(r_count);

end architecture Behavioral;
